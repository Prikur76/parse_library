import logging
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import tools

logger = logging.getLogger(__name__)


def collects_books_ids(page_url):
    """Возвращает список ID книг на указанной странице"""
    response = tools.get_response(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return tools.fetch_books_ids_from_page(soup)



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

    parser = argparse.ArgumentParser(
        description='Скачивание книг из библиотеки  tululu.org'
    )
    parser.add_argument('--start_page', type=int, default=1,
                        help='Ввести номер первой страницы')
    parser.add_argument('--end_page', type=int, default=None,
                        help='Ввести номер последней страницы')
    args = parser.parse_args()
    start = args.start_page
    end = args.end_page + 1

    base_url = 'https://tululu.org/'

    books_ids = []
    for page in range(start, end):
        try:
            page_url = urljoin(base_url, f'/l55/{page}/')
            books_ids.append(collects_books_ids(page_url))
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Request failed with HTTPError: {http_err}")
        except requests.exceptions.ConnectionError as connection_err:
            logger.error(f"Lost HTTP connection: {connection_err}")
            time.sleep(10)

    books = []
    for book_id in books_ids:
        try:
            book_url = urljoin(base_url, f'/b{book_id}/')
            response = tools.get_response(book_url)
            book = tools.parse_book_page(response, book_id)
            books.append(book)
            tools.download_content(book['text_url'], book['book_name'],
                                   folder='books/')
            tools.download_content(book['image_url'], book['image_name'],
                                   folder='images/')
        except AttributeError as attr_err:
            logger.error(f"BOOK ID: {book_id} -> AttributeError: {attr_err}")
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"BOOK ID: {book_id} -> HTTPError: {http_err}")
        except requests.exceptions.ConnectionError as connection_err:
            logger.error(f"Lost HTTP connection: {connection_err}")
            time.sleep(10)

    tools.publish_books_to_console(books)
    tools.download_books_to_file(books)

    return


if __name__ == '__main__':
    main()
