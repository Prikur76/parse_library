import os
import requests
from bs4 import BeautifulSoup
import re
from pathvalidate import sanitize_filename, validate_filepath


def fetch_text_from_library(url, book_id):
    """ TODO """
    payload = {
        'id': book_id
    }
    response = requests.get(url=url, params=payload)
    print(response.status_code)
    response.raise_for_status()
    return response


def check_for_redirect(response):
    """TODO"""
    if response.history:
        raise requests.exceptions.HTTPError(response.history[0])
    return response


def download_book(filename, book_text):
    """Записываем файл"""
    with open(filename, 'wb') as file:
        file.write(book_text)

def download_text(url, book_id, folder='books/'):
    """Функция для скачивания текстовых файлов."""
    title_url = 'b'.join([url.split('txt.php')[0], str(book_id)])
    print(title_url)
    response = requests.get(url=title_url)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('table', class_='tabs').find('td', class_='ow_px_td').find('div', id='content').find('h1').text
    title = title_tag.split(' :: ')[0].strip()
    filename = sanitize_filename(f'{title}.txt')
    filepath = os.path.join(folder, filename)
    return filepath


def main():
    url = 'https://tululu.org/txt.php'
    books_path = './books/'
    if not os.path.exists(books_path):
        os.makedirs(books_path)
    for book_id in range(1, 11):
        try:
            response = fetch_text_from_library(url, book_id)
            if check_for_redirect(response):
                book_text = response.content
                filename = download_text(url, book_id)
                download_book(filename, book_text)
        except requests.exceptions.HTTPError as err:
            print(f"book_id {book_id}: {err}")
    return


if __name__ == '__main__':
    main()

    # url = 'https://tululu.org/txt.php'
    # book_id = '1'
    # url_1 = 'b'.join([url.split('txt.php')[0], book_id])
    # print(url_1)

    # filename = download_text(url, book_id)
    # print(filename)
