# py-script
Useful python scripts for administrative functions.

## Development

### Requirements

* git: https://git-scm.com/downloads
* Python 3: https://www.python.org/downloads/
* virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

### Getting Started

1. Install git, Python 3, and virtualenv.
1. Go to preferred workspace directory, e.g. ~/projects
1. virtualenv --python python3 --prompt presterity- venvs/presterity
1. source venvs/presterity/bin/activate
1. git clone git@github.com:presterity/py-script
1. cd py-script
1. pip install -r requirements.txt


## Script Index

### extract-raindrop-bookmarks.py

This script uses the [Raindrop API](https://raindrop.io/dev/docs) to retrieve all the bookmark data for a particular collection.
By default, the bookmarks from the [Presterity collection](https://raindrop.io/app/#/collection/2021037) are extracted. The retrieved data is written as JSON to 
stdout or to a file along with metadata about the extract itself. Run with -h for usage.

### archive-links.py

This script uses the [Wayback Machine](https://archive.org/web/) to archive all of the bookmarks from a particular raindrop collection. By default, the bookmarks from the [Presterity collection](https://raindrop.io/app/#/collection/2021037) are archived. The archived URLs are written as JSON to stdout or to a file. Run with -h for usage.

## Module Index

### raindrop_api.py

General-purpose API for retrieving bookmarks from the [Raindrop API](https://raindrop.io/dev/docs)

### wayback_api.py

General-purpose API for accessing the [Wayback Machine](https://archive.org/web/)
