#!/usr/bin/env python3
print(__file__)
import sys, os, time
from datetime import datetime, timedelta

import requests
import concurrent.futures
from pymongo import MongoClient

from cli_args import conf
from logger import log
from utils import new_doc, create_file, update_db, scrape_urls

print(os.getcwd())


def crawl_link(collection, url):
	# skip crawling if crawled within last 24 hours
	doc = collection.find_one({"link" : url})
	if doc is not None and doc['isCrawled'] and\
		doc['lastCrawledDT'] > datetime.now() - timedelta(days=1):
			log.info(f' The url is already crawled within last 24hr')
			return
	
	# make connection requests to url
	try:
		req = requests.get(url)
	except OSError as exc:
		log.info(f" Error occured with {url} at time {datetime.now()}. Following error occured :\n{exc}\nSkipping...")
		return
	
	if req.status_code != 200:
		log.debug(f" \t\t\t{url} gave response code {req.status_code}")
		update_db(collection, url, src_url, req)
		return

	# create html file after successful request
	if 'text/html' in req.headers['content-type']:
		html_doc = req.text
		file_path, file_created_DT = create_file(html_doc, conf.file_dir, conf.path, 'utf-8')
	else:
		log.info(f' Not html.. ignored')
		return

	# update the database information
	update_db(collection, url, src_url, req, file_path, file_created_DT)

	# return the html document for scraping purposes
	return html_doc


def main(collection, doc, src_url):
    # get the current url
    url = doc['link']
    log.info(f" Crawling {url}")
    
    # crawl the current link
    html_doc = crawl_link(collection, url)
    if html_doc is None: return

    # scrape and extract new links from the received html document
    scrape_urls(collection, html_doc, url, src_url)


if __name__ == "__main__":
	client = MongoClient(conf.client)
	db = client[conf.database]
	collection = db[conf.collection]
	log.info(f' Connected to client : {client}\nUsing database : {db}, collection : {collection}')

	src_url = url = conf.root_url or input()
	doc = collection.find_one({"link" : url})
	if not doc:
		log.info(f" Starting afresh, creating new doc for {url} ...")
		doc_id = new_doc(collection, url, src_url)
	elif doc['lastCrawledDT'] > datetime.now() - timedelta(days=1):
		log.info(f' The link {url} is already crawled within last 24hr...')
	else:
		log.info(f" The doc for {url} is old, updating the doc...")
		collection.find_one_and_update({"link" : url}, {"$set" : {"src_link" : src_url, "isCrawled" : False}})

	while True:
		# filter the links of interest
		if collection.count_documents({"isCrawled" : False}) is not 0:   # {"$and" : [{"src_link" : src_url}, {"isCrawled" : False}] }
			log.info(" Crawling uncrawled links")
			next_docs = collection.find({"isCrawled" : False})   # {"$and" : [{"src_link" : src_url}, {"isCrawled" : False}] }
		elif collection.count_documents({"lastCrawledDT" : {"$gt" : datetime.now() - timedelta(days=1)}}) is not 0:
			log.info(" Crawling older links...")
			next_docs = collection.find({"lastCrawledDT" : {"$gt" : datetime.now() - timedelta(days=1)}})
		else:
			log.info(" All done for the day...")
	
		for doc in next_docs:
			# list of workers
			docs = [doc]

			for i, doc in enumerate(next_docs):
				docs += [doc]
				if i > 4: break
			
			with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
				future_to_doc = { executor.submit(main, collection, doc, src_url) : doc for doc in docs }
				for future in concurrent.futures.as_completed(future_to_doc):
					doc = future_to_doc[future]
					try:
						data = future.result()
					except Exception as exc:
						pass

		log.info(" Waiting 5 seconds...")
		time.sleep(5)