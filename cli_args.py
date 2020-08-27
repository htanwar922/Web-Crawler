#!/usr/bin/env python3

import sys, os, argparse
from pathlib import Path

from config import *

parser = argparse.ArgumentParser()

# running path
parser.add_argument('--path', type=str, default=os.path.dirname(__file__))
# root url
parser.add_argument('--root_url', type=str, default=config['root_url'])
# extract only, no scraping
parser.add_argument('--extract_only/', dest='extract_only', action='store_true', default=config['extract_only'])
# user MongoClient
parser.add_argument('--client', type=str, default=config['client'])
# database name
parser.add_argument('--database')

# logging level
parser.add_argument('--debug/', dest='debug', action='store_true', default=config['debug'])
# log file
parser.add_argument('--log_file', type=str, default=config['log_file'])
# log user
parser.add_argument('--log_user', type=str, default=config['log_user'])
# max size of database
parser.add_argument('--max_db_size', type=int, default=config['max_db_size'])
# max links to crawl per root url
parser.add_argument('--max_links_per_root', type=int, default=config['max_links_per_root'])
# max links to scrape from each scraped document
parser.add_argument('--max_links_per_scraped_doc', type=int, default=config['max_links_per_scraped_doc'])
# directory to store files (absolute path)
parser.add_argument('--file_dir', type=str, default=config['file_dir'])

conf = parser.parse_args()

os.chdir(Path(conf.path) or os.path.dirname(__file__))

if __name__ == "__main__":
    pass