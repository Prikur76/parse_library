import argparse
import logging
import os
import time
from urllib.parse import urljoin

import requests

import tools
import exceptions

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
        level=logging.INFO
    )

    base_url = 'https://tululu.org'

    books_path = './books/'
    image_path = './images/'
    os.makedirs(books_path, exist_ok=True)
    os.makedirs(image_path, exist_ok=True)

    parser = argparse.ArgumentParser(
        description='Скачивание книг из библиотеки  tululu.org'
    )
    parser.add_argument('start_id', nargs='?', type=int, default=1,
                        help='Ввести номер первой книги')
    parser.add_argument('end_id', nargs='?', type=int, default=1,
                        help='Ввести номер последней книги')
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id + 1

    books = []
    for book_id in range(start_id, end_id, 1):
        try:

            book_url = urljoin(base_url, f'/b{book_id}/')
            response = tools.get_response(book_url)
            book = tools.parse_book_page(response)
            books.append(book)

            tools.download_content(book['text_url'], book['book_name'],
                                   folder='books/')
            tools.download_content(book['image_url'], book['image_name'],
                                   folder='images/')

        except exceptions.NoTagError as my_err:
            logger.error(f'BOOK: {book_id} -> NoTagError: {my_err}')

        except requests.exceptions.HTTPError as http_err:
            logger.error(f'BOOK ID: {book_id} -> HTTPError: {http_err}')

        except requests.exceptions.ConnectionError as connection_err:
            logger.error(f'Lost HTTP connection: {connection_err}')
            time.sleep(10)

    tools.publish_books_to_console(books)


if __name__ == '__main__':
    main()
