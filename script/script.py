import requests
import json
from requests_html import HTMLSession

KEYWORDS = ['programming', 'software', 'javascript', 'typescript', 'java',
            'go', 'vue', 'stock', 'financial', 'economics', 'economy', 'hacker',
            'html', 'css', 'devops', 'unix', 'linux', 'script', 'hacking', 'front end',
            'frontend', 'backend', 'back end', 'cloud', 'cybersecurity', 'crypto', 'cryptography', 'entrepreneur']
API_URL = 'http://localhost:5000/findBooks'
HUMBLE_BUNDLE_URL = 'https://www.humblebundle.com/books'
TAG = 'humble bundle'
PARAM = 'target'
PARAMS = {PARAM: TAG}
r = requests.get(url=API_URL, params=PARAMS)
EXCLUDE_LIST = set(r.json())
session = HTMLSession()
response = session.get(HUMBLE_BUNDLE_URL)
BUNDLE_INFO = json.loads(response.html.find(
    '#landingPage-json-data')[0].text)['data']['books']['mosaic'][0]['products']
for bundle in BUNDLE_INFO:
    name = bundle['tile_name'].lower()
    suffix = bundle['product_url']
    if any(s in name for s in KEYWORDS):
        book_url = f"https://www.humblebundle.com{suffix}"
        response = session.get(book_url).html.find(
            '.main-content-row.dd-game-row.js-nav-row > .u-constrain-width')
        books = set()
        for item in response:
            bundle_cost = item.find(
                '.dd-header > h2')[0].text.split(' ', 2)[1] + ' Bundle'
            for book in item.find('.front-page-art-image-text'):
                books.add(book.text)
            unique_books = books - EXCLUDE_LIST
            duplicated_books = books & EXCLUDE_LIST
            if len(unique_books) > 0:
                print(f'Bundle: {bundle_cost}')
                print(f'Unique: {list(unique_books)}')
                print(f'Duplicated: {list(duplicated_books)}')
                print(f'URL: {book_url}')
