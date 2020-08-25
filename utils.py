#!/usr/bin/env python3


import sys, os, time
from datetime import datetime, timedelta
import queue, requests
import threading

import bs4 as BeautifulSoup
from pymongo import MongoClient, ReturnDocument, IndexModel, InsertOne, DeleteOne, DeleteMany, UpdateOne, UpdateMany, ReplaceOne

def parse_request_date_time(req):
	return datetime.strptime(r.headers['date'], '%a, %d %b %Y %H:%M:%S GMT')

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


def create_file(req):
	pass
	# generate random name and save the req content to path
	return html_doc, file_path, file_created_at


def update_db(collection, url, src_url, req, file_path, file_created_at):
	collection.update_one({'url' : url},
							{'$set' : {
									"link" : url,
									"src_link" : src_url,
									"isCrawled" : True,
									"lastCrawledDT" : parse_request_date_time(req),
									"responseStatus" : req.status_code,
									"contentType" : req.headers['content-type'],
									"contentLength" : 0,
									"filePath" : file_path,
									"createdAt" : file_created_at
							}})


def scrape_url(html_doc):
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
		newQ.put(tag.get('href'))
	return newQ