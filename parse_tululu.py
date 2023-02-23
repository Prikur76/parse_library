import argparse
import logging
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


logger = logging.getLogger(__name__)


def download_content(url, file_name, folder='books/'):
    """Функция для скачивания файлов в заданную папку"""
    response = requests.get(url=url)
    response.raise_for_status()
    if not response.history:
        filepath = os.path.join(folder, file_name)
        with open(filepath, 'wb') as file:
            file.write(response.content)


def get_soup(response):
    """Возвращает обработанный response в виде объекта soup"""
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def fetch_text_url(base_url, soup):
    """Возвращает словарь тэгов 'a' из ответа сайта"""
    a_tags = []
    if soup.find('div', id='content'):
        a_tags = soup.find('table', class_='d_book').find_all('a')
    for tag in a_tags:
        if tag.text == 'скачать txt' and soup.find('div', class_='bookimage'):
            return urljoin(base_url, tag.get('href'))


def fetch_image_url_and_name(base_url, soup):
    """Возвращает ссылку для скачивания изображения и имя файла"""
    image = soup.find('div', class_='bookimage').find('img')
    image_url = urljoin(base_url, image.get('src'))
    image_name = image.get('src').split('/')[-1]
    return image_url, image_name


def fetch_title_and_author(soup):
    """Возвращает название книги и автора"""
    title_tag = soup.find('h1').text
    title = title_tag.split(' :: ')[0].strip()
    author = title_tag.split(' :: ')[1].strip()
    return title, author


def fetch_genres(soup):
    """Возвращает жанр книги"""
    genres_tags = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres_tags]
    return genres


def fetch_comments(soup):
    """Возвращает список комментариев или пустой список"""
    comments_tags = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in comments_tags]
    return comments


def parse_book_page(base_url, book_id):
    """Возвращает информацию о книге в виде словаря"""
    book_url = urljoin(base_url, f'b{book_id}')
    response = requests.get(url=book_url)
    response.raise_for_status()

    if not response.history:
        raise requests.exceptions.HTTPError(response.history[0])

    decoded_response = response.text
    if 'error' in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response['error'])

    soup = get_soup(response)
    text_url = fetch_text_url(base_url, soup)
    if text_url:
        image_url_and_name = fetch_image_url_and_name(base_url, soup)
        title_and_author = fetch_title_and_author(soup)

        image_url, image_name = image_url_and_name[0], image_url_and_name[1]
        title, author = title_and_author[0], title_and_author[1]

        genres = fetch_genres(soup)
        book_name = sanitize_filename(f'{title}.txt')
        comments = fetch_comments(soup)

        book = {
            'book_id': book_id, 'text_url': text_url, 'image_url': image_url,
            'image_name': image_name, 'title': title, 'author': author,
            'genres': genres, 'book_name': book_name, 'comments': comments
        }
        return book


def publish_books_to_console(books):
    """Выводит на экран список книг"""
    print(f'\n  Всего получено {len(books)} книг.\n')
    for number, book in enumerate(books, start=1):
        print(f"   Книга № {number}.\n   Название: {book['title']}.\n   "
              f"Автор: {book['author']}")
        if book['comments']:
            print('   Комментарии:')
            for comment in book['comments']:
                print("    -", comment)
        print()


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    base_url = 'https://tululu.org'

    books_path = './books/'
    os.makedirs(books_path, exist_ok=False)

    image_path = './images/'
    os.makedirs(image_path, exist_ok=False)

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
    while start_id < end_id:
        try:
            book = parse_book_page(base_url, start_id)
            if book:
                download_content(book['text_url'], book['book_name'],
                                 folder='books/')
                download_content(book['image_url'], book['image_name'],
                                 folder='images/')
                books.append(book)
            start_id += 1

        except requests.exceptions.ConnectionError:
            logger.error("Lost HTTP connection")
            time.sleep(10)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTPError: {http_err}")

    publish_books_to_console(books)


if __name__ == '__main__':
    main()
