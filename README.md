# py-script
Useful python scripts for administrative functions.

## Development

### Requirements

* Python 3: https://www.python.org/downloads/
* virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

### Getting Started

1. Install Python 3 and virtualenv.
1. Go to preferred workspace directory.
2. virtualenv venvs/presterity
3. source venvs/presterity/bin/activate
4. git clone git@github.com:/presterity/py-script
5. pip install -r requirements.txt


## Script Index

## extract-raindrop-bookmarks.py

This script uses the [Raindrop API](https://raindrop.io/dev/docs) to retrieve all the bookmark data for a particular collection.
By default, the bookmarks from the [Presterity collection](https://raindrop.io/app/#/collection/2021037) are extracted. The retrieved data is written as JSON to 
stdout or to a file along with metadata about the extract itself. Run with -h for usage.

