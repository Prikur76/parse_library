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
        format="[%(levelname)s] - %(asctime)s - %(name)s - %(message)s",
        level=logging.INFO
    )
    dir_path = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser(
        description="""\
        Скачивание книг из раздела научной фантастики библиотеки tululu.org
        """
    )
    parser.add_argument('--start_page', type=int, default=1,
                        help='Ввести номер первой страницы')
    parser.add_argument('--end_page', type=int, default=1,
                        help='Ввести номер последней страницы')
    parser.add_argument('--dest_folder', default=dir_path,
                        help='Указать путь к каталогу с результатами парсинга')
    parser.add_argument('--json_path', default=dir_path,
                        help='Указать свой путь к *.json файлу с результатами')
    parser.add_argument('--skip_imgs', action='store_true',
                        help='Hе скачивать картинки')
    parser.add_argument('--skip_txt', action='store_true',
                        help='Не скачивать книги')

    args = parser.parse_args()
    start = args.start_page
    end = args.end_page
    if start >= end:
        end = tools.get_last_page_number() + 1
    skip_txt = args.skip_txt
    skip_imgs = args.skip_imgs
    destination = args.dest_folder
    books_file_path = args.json_path

    books_path = os.path.join(destination, 'books\\')
    images_path = os.path.join(destination, 'images\\')

    os.makedirs(books_path, exist_ok=True)
    os.makedirs(images_path, exist_ok=True)

    base_url = 'https://tululu.org/'

    books_urls = []
    for page in range(start, end, 1):
        try:
            print(page)
            page_url = urljoin(base_url, f'/l55/{page}/')
            page_books_urls = tools.fetch_books_urls_from_page(page_url)
            books_urls.extend(page_books_urls)

        except exceptions.NoTagError as my_err:
            logger.error(f"PAGE: {page} -> NoTagError: {my_err}")

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Request failed with HTTPError: {http_err}")

        except requests.exceptions.ConnectionError as connection_err:
            logger.error(f"Lost HTTP connection: {connection_err}")
            time.sleep(10)

    books = []
    for book_url in books_urls:
        try:
            response = tools.get_response(book_url)
            book = tools.parse_book_page(response)
            books.append(book)
            if not skip_txt:
                tools.download_content(book['text_url'], book['book_name'],
                                       folder=books_path)
            if not skip_imgs:
                tools.download_content(book['image_url'], book['image_name'],
                                       folder=images_path)
            print(book_url)
        except exceptions.NoTagError as my_err:
            logger.error(f"BOOK: {book_url} -> NoTagError: {my_err}")
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"BOOK: {book_url} -> HTTPError: {http_err}")
        except requests.exceptions.ConnectionError as connection_err:
            logger.error(f"Lost HTTP connection: {connection_err}")
            time.sleep(10)
    tools.publish_books_to_console(books)
    tools.download_books_to_file(books, books_file_path)


if __name__ == '__main__':
    main()
