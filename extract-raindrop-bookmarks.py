"""
Script to retrieve all links from Raindrop Presterity collection.
"""

import argparse
from datetime import datetime
import json
import logging
import sys
from typing import List, Tuple

import requests

log = None

RAINDROP_BOOKMARK_API = 'https://raindrop.io/api/raindrops/{collection_id}'
PAGE_SIZE = 40  # max number of results per page 
PRESTERITY_COLLECTION_ID = 2021037


def extract_bookmarks(collection_id: int) -> None:
    """Retrieve all bookmarks in specified collection; write results as JSON to stdout.

    For documentation on bookmark JSON: https://raindrop.io/dev/docs#bookmarks
    
    :param collection_id: int that is Raindrop collection id
    """
    page_number = 0
    bookmarks, collection_size = get_bookmarks_on_page(collection_id, page_number=page_number)
    bookmarks_retrieved = len(bookmarks)
    collection_data = {'collection_id': collection_id,
                       'request_date': datetime.utcnow().isoformat(),
                       'length': collection_size,
                       'items': bookmarks}

    while bookmarks_retrieved < collection_size:
        page_number += 1
        bookmarks, new_size = get_bookmarks_on_page(collection_id, page_number=page_number)
        if new_size != collection_size:
            raise ValueError("Collection changed size during extract; please re-run")
        bookmarks_retrieved += len(bookmarks)
        collection_data['items'].extend(bookmarks)

    # Serialize data and write to stdout
    sys.stdout.write(json.dumps(collection_data))
    

def get_bookmarks_on_page(collection_id: int, page_number: int=0 ) -> Tuple[List[dict], int]:
    """Retrieve collection bookmarks for specified page number.

    :param collection_id: int that is Raindrop collection id
    :param page_number: optional int that is page number; default is 0

    :return: list of JSON objects that are Raindrop bookmarks
    """
    uri = RAINDROP_BOOKMARK_API.format(collection_id=collection_id)
    query_params = {'page': page_number, 'perpage': PAGE_SIZE}
    log.debug("Making request to %s", uri)
    response_data = requests.get(uri, params=query_params).json()
    items = response_data.get('items', [])
    total_item_count = response_data.get('count')
    log.debug("Retrieved %d of %d bookmarks", len(items), total_item_count)
    return items, total_item_count

def build_parser() -> argparse.ArgumentParser:
    """Construct argument parser for script.

    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(description=__doc__)
    help_msg = 'id of Raindrop collection of interest; default is {0} (Presterity)'.format(
        PRESTERITY_COLLECTION_ID)
    parser.add_argument('--collection', '-c', type=int, default=PRESTERITY_COLLECTION_ID, 
                        help=help_msg)
    help_msg = 'number of requested bookmarks per query; default is {0} (max allowed)'.format(
        PAGE_SIZE)
    parser.add_argument('--page-size', '-s', type=int, default=PAGE_SIZE, help=help_msg)
    parser.add_argument('--outfile', '-o', help='file for results; default is stdout')
    parser.add_argument('--verbose', '-v', action='store_true', help='log level DEBUG')
    return parser

# def init_logging(verbose: bool=False, very_verbose: bool=False) -> logging.Logger:
#     """Initialize logging at requested verbosity.

#     :param verbose: True if script should log at DEBUG level
#     :param very_verbose: True if script and other modules should log at DEBUG level
#     :return: module-level logger
#     """
#     # Log at WARN overall unless very_verbose logging is requested; 
#     # DEBUG is very verbose for python-twitter code
#     overall_log_level = logging.WARN
#     if very_verbose:
#         overall_log_level = logging.DEBUG

#     module_log_level = logging.INFO
#     if verbose or very_verbose:
#         module_log_level = logging.DEBUG

#     logging.basicConfig(level=overall_log_level)
#     log = logging.getLogger(__name__)
    # log.setLevel(module_log_level)
    # return log

if __name__ == '__main__':
    args = build_parser().parse_args()
#    log = init_logging(verbose=args.verbose, very_verbose=args.very_verbose)
    logging.basicConfig(level=logging.WARN)
    log = logging.getLogger(__name__)
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    # Set module-level constant PAGE_SIZE
    PAGE_SIZE = args.page_size

    # Redirect stdout to outfile, if specified
    if args.outfile:
        sys.stdout = open(args.outfile, 'w')

    extract_bookmarks(args.collection)
    sys.exit(0)
