# py-script
Useful python scripts for administrative functions.

Before running scripts, install required libraries:
```bash
pip3 install -r requirements.txt
```

## extract-raindrop-bookmarks.py

This script uses the Raindrop API to retrieve all the bookmark data for a particular collection.
By default, it extracts the Presterity collection. The retrieved data is written as JSON to 
stdout or to a file along with metadata about the extract itself. Run with -h for usage.

