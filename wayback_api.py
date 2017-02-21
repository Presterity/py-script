"""
Module for accessing the web archive wayback machine (https://archive.org/web/)
"""
from typing import List, Tuple
import requests

# undocumented API scraped from the 'save page' form here: https://archive.org/web/
SAVE_PAGE_API  = 'http://web.archive.org/save/{url}'
# see: https://archive.org/help/wayback_api.php
CHECK_PAGE_API = 'http://archive.org/wayback/available'

def check_url(url: str) -> str:
    """
    Check that a URL is archived

    :param url: the URL to check
    :return: the archived URL, or None if not archived
    """
    response_data = requests.get(CHECK_PAGE_API, params={'url': url}).json()
    return response_data.get('archived_snapshots', {}).get('closest', {}).get('url', None)


def archive_url(url: str) -> str:
    """
    Archive a URL

    :param url: the URL to archive
    :return: the newly archived URL, or None if there was a problem archiving it
    """
    save_url = SAVE_PAGE_API.format(url=url)
    response = requests.get(save_url)

    if response.status_code is not 200:
        return None # TODO: return the error to be handled later

    return check_url(url)

def check_and_archive_url(url: str) -> str:
    """
    Check to see if a URL is archived. If it is, return the archived URL. If it isn't, archive it and then return the archived URL.

    :param url: the URL to check (and archive if not already)
    :return: the URL that has been archived, or None if there was a problem archiving it
    """
    archived = check_url(url)
    if archived is None:
        return archive_url(url)
    else:
        return archived