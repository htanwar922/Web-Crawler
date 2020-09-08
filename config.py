#!/usr/bin/env python3
print(__file__)
config = {
		'path' : None,
		'root_url' : 'https://flinkhub.com',
		'extract_only' : False,
		'client' : 'mongodb://localhost:27017/',
		'database' : 'mydb',
		'collection' : 'mycol',
		'debug' : True,
		'log_file' : './log.txt',
		'log_user' : '__WebCrawler__',
		'max_db_size' : 1000000,
		'file_dir' : '../files',				# relative to 'path' above
		'continue_left_off' : False
	}

default = {
		'path' : None,
		'root_url' : None,
		'extract_only' : False,
		'client' : 'mongodb://localhost:27017/',
		'database' : None,
		'collection' : None,
		'debug' : False,
		'log_file' : './log.txt',
		'log_user' : '__WebCrawler__',
		'max_db_size' : None,
		'file_dir' : '../files',				# relative to 'path' above
		'continue_left_off' : False
	}
