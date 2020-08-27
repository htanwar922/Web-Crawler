#!/usr/bin/env python3

config = {
		'path' : None,
		'root_url' : 'https://flinkhub.com',
		'extract_only' : False,
		'client' : 'mongodb://localhost:27017/',
		'debug' : True,
		'log_file' : './log.txt',
		'log_user' : '__WebCrawler__',
		'max_db_size' : 1000000,
		'max_links_per_root' : 100000,
		'max_links_per_scraped_doc' : 5,
		'file_dir' : '../files'				# relative to 'path' above
	}

default = {
		'path' : None,
		'root_url' : None,
		'extract_only' : False,
		'client' : 'mongodb://localhost:27017/',
		'debug' : False,
		'log_file' : './log.txt',
		'log_user' : '__WebCrawler__',
		'max_db_size' : 1000000,
		'max_links_per_root' : 100000,
		'max_links_per_scraped_doc' : 5000,
		'file_dir' : '../files'
	}