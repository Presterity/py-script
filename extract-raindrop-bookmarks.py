"""
Script to retrieve all links from Raindrop Presterity collection.
"""
import argparse
import json
import logging
import sys
from raindrop_api import extract_bookmarks

log = logging.getLogger(__name__)

DEFAULT_PAGE_SIZE = 40
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
        DEFAULT_PAGE_SIZE)
    parser.add_argument('--page-size', '-s', type=int, default=DEFAULT_PAGE_SIZE, help=help_msg)
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
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    # Redirect stdout to outfile, if specified
    if args.outfile:
        sys.stdout = open(args.outfile, 'w')

    collection_data = extract_bookmarks(args.collection, args.page_size)
    # Serialize data and write to stdout
    sys.stdout.write(json.dumps(collection_data, indent = 4))

    sys.exit(0)
