import sys
import requests
import logging
import os
import json

from pytablewriter import MarkdownTableWriter

import pr_commit_request as commit_request
import pr_lines_changed as lines_changed


class DeveloperMetrics:
    """Creates the developer metrics for a PR."""
    logging.getLogger().setLevel(logging.INFO)

    def __init__(self):
        self.github_token = os.environ.get('API_KEY')
        self.headers = {'Authorization': 'token ' + self.github_token}
        if sys.argv[1]:
            self.pr_num = str(sys.argv[1])
        if sys.argv[2]:
            self.repo = str(sys.argv[2])
        self.repo_reference = "https://api.github.com/repos/" + self.repo + "/issues/"

    def create_developer_metrics(self):
        """
        Create the developer metrics for a pull request.
        """
        pr_comments_endpoint = self.repo_reference + self.pr_num + "/comments"
        table_data = self.get_markdown_table()
        data = {"body": table_data}
        resp = requests.post(pr_comments_endpoint, headers=self.headers, data=json.dumps(data))
        logging.info(resp)

    def get_markdown_table(self):
        """
        Generates the markdown table.
        """
        pr_create = commit_request.pr_stats()
        pr_create.get_pr_creation_time()
        pr_lines = lines_changed.LinesOfCode()
        writer = MarkdownTableWriter(
            table_name="Developer Metrics",
            headers=["Developer Metric", "Metric Value"],
            value_matrix=[
                ["PR create to PR review", pr_create.pr_create_to_review],
                ["Lines of code changed", pr_lines.get_lines_of_code_change()]
            ],
        )
        return writer.dumps()


def main():
    pr = DeveloperMetrics()
    pr.create_developer_metrics()


if __name__ == '__main__':
    main()
