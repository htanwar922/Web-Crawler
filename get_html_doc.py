#!/usr/bin/env python3
print(__file__)
import webbrowser

from main import collection

while True:
	url = input("Enter link to get : ")
	doc = collection.find_one({'link' : url})

	if doc is None:
		print("Link not crawled.")
	elif doc['filePath'] is None:
		print("Link was not accessible.")
	else:
		print(f"Corresponding file exists at {doc['filePath']} .")
		p = input("Open in browser? (yes|no) : ")
		if p == "yes":
			webbrowser.open(f"file://{doc['filePath']}", new=2)
			#with open(doc['filePath'], 'rb') as foo:
			#	f = foo.readlines()
			#	for l in f:
			#		print(l)
		else:
			pass
