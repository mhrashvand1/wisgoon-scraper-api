import os
import sys


def run_crawler(username, from_datetime=None):
    executable = sys.executable
    # Assume that the working directory is the same as the directory containing the manage.py module.
    command = f"cd ../scraper/ && {executable} go_spider.py -u {username}"
    if from_datetime:
        command += f' -d {from_datetime}'
    os.system(command)
