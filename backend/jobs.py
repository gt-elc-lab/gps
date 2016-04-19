import argparse

from crawler import *

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--update', help='run the crawler', action="store_true")

def get_new_posts():
    RedditCrawler(SimpleClassifier()).crawl()
    YikYakCrawler(SimpleClassifier()).crawl()


if __name__ == '__main__':
    args = parser.parse_args()
    if args.update:
        get_new_posts()
        print 'Finished getting new posts'

