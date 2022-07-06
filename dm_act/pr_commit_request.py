import sys
import requests
import logging
import os
from subprocess import check_output
from dateutil.parser import parse
from datetime import datetime


class pr_stats:
    """Defines PR stats"""
    logging.getLogger().setLevel(logging.INFO)

    def __init__(self):
        self.github_token = os.environ.get("API_KEY")
        self.headers = {'Authorization': 'token ' + self.github_token}
        if sys.argv[1]:
            self.pr_num = str(sys.argv[1])
        if sys.argv[2]:
            self.repo = str(sys.argv[2])
        self.repo_reference = "https://api.github.com/repos/" + self.repo + "/pulls/"
        self.pr_create_to_review = "Skipped execution as stats are already published."

    def get_pr_creation_time(self):
        """Gets PR creation time for a given pull request"""
        pr_endpoint = self.repo_reference + self.pr_num
        pr_details = requests.get(pr_endpoint, headers=self.headers)
        if pr_details.json():
            pr_created_at = pr_details.json().get('created_at')
            pr_creation_date = datetime.fromisoformat(pr_created_at[:-1])
            self.get_branch_first_commit(pr_creation_date)
        else:
            logging.info("Failed to fetch the PR creation date")

    def get_branch_first_commit(self, pr_create_date):
        """Gets PR first commit for a given pull request"""
        pr_commit_endpoint = self.repo_reference + self.pr_num + "/commits"
        commits_details = requests.get(pr_commit_endpoint, headers=self.headers)
        if commits_details.json():
            first_commit_date_author_date = commits_details.json()[0].get('commit', {}).get('author', {}).get('date')
            first_commit_date = datetime.fromisoformat(first_commit_date_author_date[:-1])
            self.get_date_time_difference(pr_create_date, first_commit_date, 'PR creation', 'PR first commit')
        else:
            logging.info("Failed to fetch the branch first commit date")

    def get_date_time_difference(self, first_date, second_date, first_date_type, second_date_type):
        """Gets the time difference between two dates"""
        timedelta = first_date - second_date
        logging.info("{} date is: {}".format(first_date_type, first_date))
        logging.info("{} date is: {}".format(second_date_type, second_date))
        timedelta_str = str(timedelta)
        pr_open_time_dhms = timedelta.days, int(timedelta_str[-8:-6]), int(
            timedelta_str[-5:-3]), int(timedelta_str[-2:])
        logging.info("Time between '%s' and '%s' is: %d days, %d hours, "
                     "%d minutes and %d seconds" % (first_date_type, second_date_type, pr_open_time_dhms[0],
                                                    pr_open_time_dhms[1], pr_open_time_dhms[2], pr_open_time_dhms[3]))
        self.pr_create_to_review = "{} days, {} hours, {} minutes and {} seconds"\
            .format(pr_open_time_dhms[0], pr_open_time_dhms[1], pr_open_time_dhms[2], pr_open_time_dhms[3])


def main():
    pr = pr_stats()
    pr.get_pr_creation_time()


if __name__ == '__main__':
    main()
