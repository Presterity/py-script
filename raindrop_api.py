"""
Module for accessing the raindrop.io API
"""
from datetime import datetime
import json
from typing import List, Tuple
import requests
import logging


RAINDROP_BOOKMARK_API = 'https://raindrop.io/api/raindrops/{collection_id}'
DEFAULT_PAGE_SIZE = 40  # max number of results per page 

def extract_bookmarks(collection_id: int, page_size: int=DEFAULT_PAGE_SIZE, log: logging.Logger=None) -> dict:
    """Retrieve all bookmarks in specified collection; write results as JSON to stdout.

    For documentation on bookmark JSON: https://raindrop.io/dev/docs#bookmarks
    
    :param collection_id: int that is Raindrop collection id
    """
    page_number = 0
    bookmarks, collection_size = get_bookmarks_on_page(collection_id, page_number, page_size, log)
    bookmarks_retrieved = len(bookmarks)
    collection_data = {'collection_id': collection_id,
                       'request_date': datetime.utcnow().isoformat(),
                       'length': collection_size,
                       'items': bookmarks}

    while bookmarks_retrieved < collection_size:
        page_number += 1
        bookmarks, new_size = get_bookmarks_on_page(collection_id, page_number, page_size, log)
        if new_size != collection_size:
            raise ValueError("Collection changed size during extract; please re-run")
        bookmarks_retrieved += len(bookmarks)
        collection_data['items'].extend(bookmarks)

    return collection_data
    
def get_bookmarks_on_page(collection_id: int, page_number: int=0, page_size: int=DEFAULT_PAGE_SIZE, log: logging.Logger=None) -> Tuple[List[dict], int]:
    """Retrieve collection bookmarks for specified page number.

    :param collection_id: int that is Raindrop collection id
    :param page_number: optional int that is page number; default is 0

    :return: list of JSON objects that are Raindrop bookmarks
    """
    uri = RAINDROP_BOOKMARK_API.format(collection_id=collection_id)
    query_params = {'page': page_number, 'perpage': page_size}
    if log is not None:
    	log.debug("Making request to %s", uri)
    response_data = requests.get(uri, params=query_params).json()
    items = response_data.get('items', [])
    total_item_count = response_data.get('count')
    if log is not None:
    	log.debug("Retrieved %d of %d bookmarks", len(items), total_item_count)
    return items, total_item_count
