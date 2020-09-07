#!/usr/bin/env python3
print(__file__)
import sys, os, time
from pathlib import Path
from datetime import datetime, timedelta
from queue import Queue
import threading, tempfile, requests, uuid
from bs4 import BeautifulSoup
from pymongo import MongoClient
import errno

from logger import log
from cli_args import conf

def create_dirs(dir_path):
	if dir_path and not os.path.exists(dir_path):
		try: os.makedirs(dir_path)
		except OSError as exc:
			if exc.errno != errno.EEXIST: raise


def parse_https_date_time(req):
	return datetime.strptime(req.headers['date'], '%a, %d %b %Y %H:%M:%S GMT')


def new_doc(collection, url, src_url):
	if conf.max_db_size and collection.count({}) >= conf.max_db_size:
		log.info(" Max database limit reached. Can't add new documents..")
		return
	doc_id = collection.insert_one({
				"link" : url,
				"src_link" : src_url,
				"isCrawled" : False,
				"lastCrawledDT" : None,
				"responseStatus" : None,
				"contentType" : None,
				"contentLength" : 0,
				"filePath" : None,
				"createdAt" : None
			}).inserted_id
	return doc_id


def create_file(doc, filedir=Path('../files'), filepath=None, encoding='utf-8'):
	"""
	Create unique files in dir and write the doc to it.
	Parameters :
		doc : document to write
		dir : directory where file is to be created - Path('../files') by default
		encoding : utf-8 by default
	Returns :
		file path with .html extension : str
		file creation date-time : datetime
	"""
	# generate random name and save the req content to path
	filename = str(uuid.uuid4()) + '.html'
	file_path = Path(filepath or os.getcwd()) / filedir / filename
	create_dirs(os.path.dirname(file_path))
	with open(file_path, 'w', encoding='utf-8') as foo:
		foo.write(doc)
	file_created_DT = datetime.now()
	foo.close()
	return str(file_path), file_created_DT


def update_db(collection, url, src_url, req, file_path=None, file_created_DT=None, isCrawled=True):
	doc = collection.find_one({'link' : url})
	collection.update_one({'link' : url},
							{'$set' : {
									"link" : url,
									"src_link" : src_url,
									"isCrawled" : isCrawled,
									"lastCrawledDT" : parse_https_date_time(req),
									"responseStatus" : req.status_code,
									"contentType" : req.headers['content-type'] if req.status_code == 200 else None,
									"contentLength" : 0 or doc['contentLength'],
									"filePath" : file_path or doc['filePath'],
									"createdAt" : file_created_DT or doc['createdAt']
							}})


def scrape_urls(collection, html_doc, current_url, src_url):
	"""
	Get all valid links from 'href' attribute of <a> tags in the doc. \
		New docs are created corresponding to the scraped links.
	
	Parameters :
		html_doc : str
		current_url : str : url corresponding to the html_doc
	Returns :
		None
	"""
	log.info(f" \tScraping {current_url}")
	soup = BeautifulSoup(html_doc, 'html.parser')
	tags = soup.find_all('a')[:5000]
	parent_url = '/'.join(current_url.split('/')[:3])

	for tag in tags:
		url = tag.get('href')
		if not url: continue
		# ignore invalid links
		if url.endswith(':;') or url.startswith('#'):
			continue
		# handling relative links
		if url[0] == '/':
			url = parent_url + url
		_ = new_doc(collection, url, src_url)
		#log.debug(f' \t\tinside scrape function : {url}')