#!/usr/bin/env python3

import sys, os, time
from datetime import datetime, timedelta

import requests, threading
import bs4 as BeautifulSoup
from queue import Queue

from pymongo import MongoClient

from utils import *
from cli import *

if __name__ == "__main__":
	src_url = url = input()
	Q = Queue(maxsize=10000)			# queue of links to scrape now
	nextQ = Queue()						# queue of queues of links got from just scraped document, with levels separated by a 'None' entry

	client = MongoClient()
	db = client.mydb
	collection = db.mycol

	nextQ.put(Queue(maxsize=5000).put(url))
	nextQ.put(None)

	# scrape from root url - BFS algorithm
	while not (Q.qsize() == 0 and nextQ.qsize() == 0):

		# 
		while Q.qsize() != 0:
			url = Q.get()

			# check database for already crawled url
			# if no existing doc associated, create a new one
			doc_id = check_db(collection, url)

			# skip crawling if crawled within last 24 hours
			lastCrawledDT = collecion.find_one({"_id" : doc_id})['lastCrawledDT']
			if lastCrawledDT is not None and \
				lastCrawledDT > datetime.now() - timedelta(days=1):
					continue

			# make connection requests to url
			try:
				req = requests.get(url)
			except OSError as Exception:
				log.info(f"Error occured with {url}\n{Exception}")
				continue

			# create file after successful request
			html_doc, file_path, file_created_at = create_file(req)

			# update the database information
			update_db(collection, url, src_url, req, file_path, file_created_at)

			# scrape the reuest for next data
			newQ = scrape_url(html_doc)

			# append the new queue to nextQ
			nextQ.put(newQ)

		# next queue
		if Q.qsize() == 0:
			Q = nextQ.get()

			# if the current level scraping is completed, nextQ will return None
			if Q is None:
				log.info('Level Completed. Waiting for 5 seconds...')
				time.sleep(5)

			# handle multiple None in nextQ
			while Q is None:
				if nextQ.qsize() == 0: break
				Q = nextQ.get()
				# append None to nextQ for level completion mark
				nextQ.put(None)
