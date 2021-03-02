import requests
import json
from requests_html import HTMLSession

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

KEYWORDS = ['programming', 'software', 'javascript', 'typescript', 'java',
            'go', 'vue', 'stock', 'financial', 'economics', 'economy', 'hacker',
            'html', 'css', 'devops', 'unix', 'linux', 'script', 'hacking', 'front end',
            'frontend', 'backend', 'back end', 'cloud', 'cybersecurity', 'crypto', 'cryptography', 'entrepreneur',
            "o'reilly", 'packt', 'apress', 'no starch press']
API_URL = 'https://humble.asantosdev.com/findBooks'
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
            unique_books = list(books - EXCLUDE_LIST)
            duplicated_books = list(books & EXCLUDE_LIST)
        if len(unique_books) > 0:
            print(f"{bcolors.WARNING}Bundle:{bcolors.HEADER} {bundle['tile_name']}")
            print(f'{bcolors.WARNING}URL:{bcolors.OKCYAN} {book_url}')
            print(f'{bcolors.WARNING}Unique:{bcolors.ENDC}')
            unique_books[0] = '-> '+unique_books[0]
            print(*unique_books, sep='\n-> ')
            duplicated_books[0] = '-> '+duplicated_books[0]
            print(f'{bcolors.WARNING}Duplicated:{bcolors.ENDC}')
            print(*duplicated_books, sep='\n-> ')