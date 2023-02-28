import logging
import os
import re
import time
import json

import requests
from bs4 import BeautifulSoup

import tools

logger = logging.getLogger(__name__)


def get_books_ids_from_pages(base_url, start_page=1, end_page=2):
    """Возвращает список ID книг на выбранных страницах"""
    books_ids = []
    for page in range(start_page, end_page):
        sci_fi_addition = f'/l55/{page}/'
        response = tools.get_response(base_url, sci_fi_addition)
        soup = BeautifulSoup(response.text, 'lxml')
        books_ids.extend(tools.fetch_books_ids(soup))
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

    # parser = argparse.ArgumentParser(
    #     description='Скачивание книг из библиотеки  tululu.org'
    # )
    # parser.add_argument('--start_page', type=int, default=1,
    #                     help='Ввести номер первой страницы')
    # parser.add_argument('--end_page', type=int, default=None,
    #                     help='Ввести номер последней страницы')
    # args = parser.parse_args()
    # start_id = args.start_page
    # end_id = args.end_page

    try:
        base_url = 'https://tululu.org/'
        all_books_ids = get_books_ids_from_pages(base_url, start_page=1, end_page=4)
        # sci_fi_addition = f'/l55/1/'
        # response = tools.get_response(base_url, sci_fi_addition)
        # soup = BeautifulSoup(response.text, 'lxml')
        # pages_count = 4                  # tools.fetch_pages_count(soup)
        # books_ids = tools.fetch_books_ids(soup)
        # for page in range(2, pages_count+1, 1):
        #     sci_fi_addition = f'/l55/{page}/'
        #     response = tools.get_response(base_url, sci_fi_addition)
        #     soup = BeautifulSoup(response.text, 'lxml')
        #     books_ids.extend(tools.fetch_books_ids(soup))

    except requests.exceptions.ConnectionError as connection_err:
        logger.error(f"Lost HTTP connection: {connection_err}")
        time.sleep(10)

    books = []
    for book_id in all_books_ids:
        try:
            book_addition = f'/b{book_id}/'
            response = tools.get_response(base_url, book_addition)
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
    # tools.publish_books_to_console(books)
    tools.download_books_to_file(books)

    return


if __name__ == '__main__':
    # main()
    print(type('books.json'))

    # with open("books.json", "r") as my_file:
    #     books_json = my_file.read()
    #     print(type(books_json))
    #
    # read_books = json.loads(books_json)
    # print(read_books)