#!/usr/bin/env python3

import sys, os, time
from datetime import datetime, timedelta

import requests, threading
import bs4 as BeautifulSoup
from queue import Queue

from pymongo import MongoClient

from cli_args import *
from logger import *
from utils import *

print(os.getcwd())

if __name__ == "__main__":
	src_url = url = conf.root_url or input()
	Q = Queue(maxsize=conf.max_links_per_scraped_doc)			# queue of links to scrape now
	nextQ = Queue()												# queue of queues of links got from just scraped document, with levels separated by a 'None' entry
	
	client = MongoClient(conf.client)
	db = client.mydb
	collection = db.mycol
	log.debug(f' Connected to client : {client}')

	Q.put(url)
	nextQ.put(Q)
	nextQ.put(None)
	db_size_override = False
	
	# scrape from root url - BFS algorithm
	while not (Q.qsize() == 0 and nextQ.qsize() == 0):
		# database limit
		if collection.count() > conf.max_db_size and not db_size_override:
			log.info('Max database size reached...')
			if input('Override [y/n] : ') != 'y':
				continue
			db_size_override = True

		# till current query is done
		while Q.qsize() != 0:
			url = Q.get()
			log.debug(f' url : {url}')
			
			# check database for already crawled url
			# if no existing doc associated, create a new one
			doc_id = check_db(collection, url, src_url)

			# skip crawling if crawled within last 24 hours
			lastCrawledDT = collection.find_one({"_id" : doc_id})['lastCrawledDT']
			if lastCrawledDT is not None and \
				lastCrawledDT > datetime.now() - timedelta(days=1):
					continue

			# make connection requests to url
			try:
				req = requests.get(url)
			except OSError as Exception:
				log.info(f"Error occured with {url}\n{Exception}")
				continue

			# if status not ok
			if req.status_code != 200: continue

			# create html file after successful request
			if 'text/html' in req.headers['content-type']:
				html_doc = req.text
				file_path, file_created_DT = create_file(html_doc, conf.file_dir, conf.path, 'utf-8')
			else:
				continue

			# update the database information
			update_db(collection, url, src_url, req, file_path, file_created_DT)

			# scrape the reuest for next data
			newQ = scrape_url(html_doc, url)

			# append the new queue to nextQ
			nextQ.put(newQ)

		# next queue
		if Q.qsize() == 0:
			Q = nextQ.get()

			# if the current level scraping is completed, nextQ will return None
			if Q is None:
				log.info(' Level Completed. Waiting for 5 seconds...')
				time.sleep(5)

			# handle multiple None in nextQ
			while Q is None:
				log.debug(' Q is None.')
				if nextQ.qsize() == 0: log.info(' All done...'); break
				Q = nextQ.get()
				# append None to nextQ for level completion mark
				nextQ.put(None)
