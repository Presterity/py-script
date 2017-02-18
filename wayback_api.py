"""
Module for accessing the web archive wayback machine (https://archive.org/web/)
"""
from typing import List, Tuple
import requests

# undocumented API scraped from the 'save page' form here: https://archive.org/web/
SAVE_PAGE_API  = 'http://web.archive.org/save/{url}'
# see: https://archive.org/help/wayback_api.php
CHECK_PAGE_API = 'http://archive.org/wayback/available'

def archive_url(url: str) -> str:
	"""
	Check that a URL is archived. If it isn't already, archive it and return the archive URL.
	"""
	print("archiving url ", url)
	response_data = requests.get(CHECK_PAGE_API, params={'url': url}).json()
	archived_url = response_data.get('archived_snapshots', {}).get('closest', {}).get('url', None)
	if archived_url is None:
		# 1. go add it
		save_url = SAVE_PAGE_API.format(url=url)
		response = requests.get(save_url)
		# throw exception if response was not 200 OK
		response.raise_for_status() 
		# 2. look it up again
		return archive_url(url) # TODO: limit retries
	else:
		return archived_url

