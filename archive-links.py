"""
Script to ensure that all bookmarks from raindrop have been archived in the Way Back Machine (https://archive.org/web/)
"""
from typing import List, Callable, Tuple
import json
import sys
from raindrop_api import extract_bookmarks
from wayback_api import archive_url

PRESTERITY_COLLECTION_ID = 2021037
# undocumented API scraped from the 'save page' form here: https://archive.org/web/
SAVE_PAGE_API  = 'http://web.archive.org/save/{url}'
# see: https://archive.org/help/wayback_api.php
CHECK_PAGE_API = 'http://archive.org/wayback/available'

def archive_urls(urls: List[str], cb: Callable[[dict], None]) -> None:
	"""
	Batch archive a list of URLs

	:param urls: list of URLs to archive
	:param cb: a callback that is executed each time a URL is successfully archived. The callback is given the argument: {original: <url>, archive: <url>}
	"""
	for url in urls:
		if "?" in url:
			print("skipping url ", url)
		else:
			data = {'original': url, 'archive': archive_url(url)}
			cb(data)

if __name__ == '__main__':
	raindrop_collection = extract_bookmarks(PRESTERITY_COLLECTION_ID)
	bookmarks = raindrop_collection.get('items', [])
	f = lambda x: x.get('link', '')
	urls = list(map(f, bookmarks))
	archive_urls(urls, lambda x: print(json.dumps(x)))
