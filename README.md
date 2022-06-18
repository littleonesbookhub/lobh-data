# lobh-data
Image scraping

## Dev environment

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you pip install any new packages, please remember to run:

```
pip freeze > requirements.txt
```

and commit requirements.txt to the repository.

## Running the code

To manually annotate the description and image thumbs from Google Books, run the following script:
```
python Imagescrape.py
```

To automatically annotate the image thumbs and genres from Good Reads, run the following script:
```
python good_reads.py
```