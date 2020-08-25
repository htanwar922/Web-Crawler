#!/usr/bin/env python3

import sys, os, logging, argparse, errno
from pathlib import Path

from config import *

os.chdir(os.path.dirname(Path(__file__)))

parser = argparse.ArgumentParser()
# root url
parser.add_argument('--root_url', type=str, default='https://flinkhub.com')
# extract only, no scraping
parser.add_argument('--extract_only/', dest='extract_only', action='store_true', default=False)
# user MongoClient
parser.add_argument('--client', type=str, default='mongodb://localhost:27017/')
# logging level
parser.add_argument('--debug/', dest='debug', action='store_true', default=False)
# log file
parser.add_argument('--log_file', type=str, default='./log.txt')
# log user
parser.add_argument('--log_user', type=str, default='__WebCrawler__')

conf = parser.parse_args()

conf.log_file = Path(conf.log_file)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG if conf.debug else logging.INFO)
log = logging.getLogger(conf.log_user)

if not os.path.isdir(os.path.dirname(conf.log_file)): os.mkdir(os.path.dirname(conf.log_file))
open(conf.log_file, 'w').close()

if not os.path.exists(os.path.dirname(conf.log_file)):
    try: os.makedirs(os.path.dirname(conf.log_file))
    except OSError as exc:
        if exc.errno != errno.EEXIST: raise # Guard against race condition

with open(conf.log_file, "w") as f: pass

fh = logging.FileHandler(conf.log_file)  #Path(conf.saved_models) / 'log.txt'
log.addHandler(fh)

if __name__ == "__main__":
    pass