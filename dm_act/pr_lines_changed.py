import sys
import requests
import logging
import os


class LinesOfCode:
    """Checks the lines of code change in PR"""
    logging.getLogger().setLevel(logging.INFO)

    def __init__(self):
        self.github_token = os.environ.get('API_KEY')
        self.headers = {'Authorization': 'token ' + self.github_token}
        if sys.argv[1]:
            self.pr_num = str(sys.argv[1])
        if sys.argv[2]:
            self.repo = str(sys.argv[2])
        self.repo_reference = "https://api.github.com/repos/" + self.repo + "/pulls/"

    def get_lines_of_code_change(self):
        """
        Get the total lines of code changed in a PR.
        """
        total_lines = 0
        pr_endpoint = self.repo_reference + self.pr_num
        pr_details = requests.get(pr_endpoint, headers=self.headers)
        if pr_details.json():
            lines_added = pr_details.json().get("additions")
            lines_deleted = pr_details.json().get("deletions")
            total_lines = lines_added + lines_deleted
            logging.info("PR Number is: 'https://github.com/AudaxHealthInc/cycletime/pull/{}'".format(self.pr_num))
            logging.info("Total lines of code changed: {}.".format(total_lines))
            logging.info("Number of lines added: {}.".format(lines_added))
            logging.info("Number of lines deleted: {}.".format(lines_deleted))
        else:
            logging.info("Failed to fetch lines of code changed in the PR: {}.".format(self.pr_num))
        return total_lines


def main():
    pr = LinesOfCode()
    pr.get_lines_of_code_change()


if __name__ == '__main__':
    main()
