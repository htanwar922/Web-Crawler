#!/usr/bin/env python3

import sys, os, time
from pathlib import Path
from datetime import datetime, timedelta
from queue import Queue
import threading, tempfile, requests, uuid
from bs4 import BeautifulSoup
from pymongo import MongoClient

from logger import *

def create_dirs(dir_path):
	if dir_path and not os.path.exists(dir_path):
		try: os.makedirs(dir_path)
		except OSError as exc:
			if exc.errno != errno.EEXIST: raise


def parse_https_date_time(req):
	return datetime.strptime(req.headers['date'], '%a, %d %b %Y %H:%M:%S GMT')

def check_db(collection, url, src_url):
	doc = collection.find_one({"url" : url})
	if doc is None:
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
	else:
		doc_id = doc['_id']
	return doc_id


def create_file(doc, dir=Path('../files'), path=None, encoding='utf-8'):
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
	file_path = Path(path or os.getcwd()) / dir / filename
	create_dirs(os.path.dirname(file_path))
	with open(file_path, 'w', encoding='utf-8') as foo:
		foo.write(doc)
	file_created_DT = datetime.now()
	foo.close()
	return str(file_path), file_created_DT


def update_db(collection, url, src_url, req, file_path, file_created_DT):
	collection.update_one({'link' : url},
							{'$set' : {
									"link" : url,
									"src_link" : src_url,
									"isCrawled" : True,
									"lastCrawledDT" : parse_https_date_time(req),
									"responseStatus" : req.status_code,
									"contentType" : req.headers['content-type'],
									"contentLength" : 0,
									"filePath" : file_path,
									"createdAt" : file_created_DT
							}})


def scrape_url(html_doc, parent_url):
	"""
	Get all links from 'href' attribute of <a> tags in the doc.
	Parameters :
		doc : str
	Returns :
		list of str (links)
	"""
	soup = BeautifulSoup(html_doc, 'html.parser')
	tags = soup.find_all('a')[:5000]

	newQ = Queue(maxsize=5000)
	for tag in tags:
		url = tag.get('href')
		if url and url[0] == '/':
			url = parent_url + url
		newQ.put(url)
		log.debug(f' inside scrape function : {url}')
	return newQ