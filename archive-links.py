"""
Script to ensure that all bookmarks from raindrop have been archived in the Way Back Machine (https://archive.org/web/)
"""
import argparse
from typing import List, Callable, Tuple
import json
import sys
from raindrop_api import extract_bookmarks
from wayback_api import check_and_archive_url
import logging

log = logging.getLogger(__name__)

DEFAUlT_PAGE_SIZE = 40
PRESTERITY_COLLECTION_ID = 2021037

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
        DEFAUlT_PAGE_SIZE)
    parser.add_argument('--page-size', '-s', type=int, default=DEFAUlT_PAGE_SIZE, help=help_msg)
    parser.add_argument('--outfile', '-o', help='file for results; default is stdout')
    parser.add_argument('--verbose', '-v', action='store_true', help='log level DEBUG')
    return parser


def archive_urls(urls: List[str], cb: Callable[[dict], None]) -> None:
    """
    Batch archive a list of URLs

    :param urls: list of URLs to archive
    :param cb: a callback that is executed each time a URL is successfully archived. 
    The callback is given the argument: {original: <url>, archive: <url>}
    """
    for url in urls:
        archived = check_and_archive_url(url)
        if archived is None:
            log.warn("unable to archive url %s", url)
            data = {'original': url}
        else:
            data = {'original': url, 'archive': archived}
        cb(data)

if __name__ == '__main__':
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.WARN)
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    raindrop_collection = extract_bookmarks(args.collection, args.page_size)
    bookmarks = raindrop_collection.get('items', [])
    urls = list(map(lambda x: x.get('link', ''), bookmarks))

    # Redirect stdout to outfile, if specified
    if args.outfile:
        sys.stdout = open(args.outfile, 'w')

    archive_urls(urls, lambda x: sys.stdout.write((json.dumps(x) + '\n')))