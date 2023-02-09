from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(
    prog='wisgoon scraper'
)
 
parser.add_argument(
    '-u', '--username',
    type=str,
    dest='username',
    help='wisgoon page username',
    required=True
)
parser.add_argument(
    '-d', '--datetime',
    type=str,
    dest='from_datetime',
    default='',
    help='Crawling posts from this date onwards'
)

args = parser.parse_args()

username = args.username
from_datetime = args.from_datetime
try:
    from_datetime = datetime.strptime(
        from_datetime,
        "%Y-%m-%dT%H:%M:%S"
    )
except:
    the_origin_of_my_history = "2001-01-20T00:00:00"
    from_datetime = datetime.strptime(
        the_origin_of_my_history,
        "%Y-%m-%dT%H:%M:%S"
    )
    
    
process = CrawlerProcess(get_project_settings())
process.crawl('wisgoon', username=username, from_datetime=from_datetime)

process.start()