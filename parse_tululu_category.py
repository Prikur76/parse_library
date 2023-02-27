import logging
import os
import re
import time

import requests
from bs4 import BeautifulSoup

import tools as t

logger = logging.getLogger(__name__)


def fetch_pages_count(soup):
    """Возвращает количество страниц"""
    pages_count = int(soup.find_all('a', class_='npage')[-1].text)
    return pages_count


def fetch_books_ids(soup):
    """Возвращает список номеров книг"""
    books_ids = []
    a_tags = soup.find('div', id='content')\
        .find_all('a', title=re.compile('скачать'))
    for tag in a_tags:
        book_id = re.findall(r'(\d+)', tag.get('href'))[0]
        books_ids.append(book_id)
    return books_ids


def main():
    logging.basicConfig(
        format="[%(levelname)s] - %(asctime)s - %(name)s - %(message)s",
        level=logging.INFO
    )

    books_path = './books/'
    image_path = './images/'
    os.makedirs(books_path, exist_ok=True)
    os.makedirs(image_path, exist_ok=True)

    base_url = 'https://tululu.org/'
    pages_count = 11
    books = []
    for page in range(1, pages_count, 1):
        sci_fi_addition = f'/l55/{page}/'
        response = t.get_response(base_url, sci_fi_addition)
        soup = BeautifulSoup(response.text, 'lxml')
        # pages_count = fetch_pages_count(soup)
        books_ids = fetch_books_ids(soup)

        for book_id in books_ids:
            try:
                book_addition = f'/b{book_id}/'
                response = t.get_response(base_url, book_addition)
                book = t.parse_book_page(response, book_id)
                books.append(book)
                t.download_content(book['text_url'], book['book_name'],
                                   folder='books/')
                t.download_content(book['image_url'], book['image_name'],
                                   folder='images/')
            except AttributeError as attr_err:
                logger.error(f"BOOK ID: {book_id} -> AttributeError: {attr_err}")
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"BOOK ID: {book_id} -> HTTPError: {http_err}")
            except requests.exceptions.ConnectionError as connection_err:
                logger.error(f"Lost HTTP connection: {connection_err}")
                time.sleep(10)
    t.publish_books_to_console(books)
    return


if __name__ == '__main__':
    main()
