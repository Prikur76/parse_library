import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_response(base_url, addition):
    """Возвращает ответ на запрос либо возбуждает исключение"""
    target_url = urljoin(base_url, addition)
    response = requests.get(url=target_url)
    response.raise_for_status()
    if response.history:
        raise requests.exceptions.HTTPError('Redirect. ', response.history)
    return response


def fetch_text_url(base_url, soup):
    """
    Возвращает ссылку для скачивания текста книги (при наличии)
    или возбуждает исключение AttributeError
    """
    tag_href = soup.find('table', class_='d_book')\
        .find('a', string='скачать txt').get('href')
    return urljoin(base_url, tag_href)


def fetch_image_url_and_name(book_url, soup):
    """Возвращает ссылку для скачивания изображения и имя файла"""
    image = soup.find('div', class_='bookimage').find('img')
    image_url = urljoin(book_url, image.get('src'))
    image_name = image.get('src').split('/')[-1]
    return image_url, image_name


def fetch_title_and_author(soup):
    """Возвращает название книги и автора"""
    title_tag = soup.find('h1').text
    title, author = title_tag.split(' :: ')
    return title.strip(), author.strip()


def fetch_genres(soup):
    """Возвращает жанр книги или пустой список"""
    genres_tags = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres_tags]
    return genres


def fetch_comments(soup):
    """Возвращает список комментариев или пустой список"""
    comments_tags = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in comments_tags]
    return comments


def parse_book_page(response, book_id):
    """
    Возвращает информацию о книге в виде словаря в случае,
    если есть ссылка для скачивания текст книги (text_url),
    либо ответ None
    """
    soup = BeautifulSoup(response.text, 'lxml')
    text_url = fetch_text_url(response.url, soup)
    image_url, image_name = fetch_image_url_and_name(response.url, soup)
    title, author = fetch_title_and_author(soup)
    genres = fetch_genres(soup)
    book_name = sanitize_filename(f'{title}.txt')
    comments = fetch_comments(soup)
    book = {
        'book_id': book_id, 'text_url': text_url, 'image_url': image_url,
        'image_name': image_name, 'title': title, 'author': author,
        'genres': genres, 'book_name': book_name, 'comments': comments
    }
    return book


def download_content(content_url, file_name, folder='books/'):
    """Функция для скачивания файлов в заданную папку"""
    response = requests.get(url=content_url)
    response.raise_for_status()
    if response.history:
        raise requests.exceptions.HTTPError('Redierct: ', response.history)

    filepath = os.path.join(folder, file_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return


def publish_books_to_console(books):
    """Выводит на экран список книг"""
    head_message = """
    Всего получено %d книг.
    """ % (len(books))
    print(tw.dedent(head_message))

    for number, book in enumerate(books, start=1):
        book_message = """\
        Книга № %d. %s
        Автор: %s
        Жанры: %s\
        """ % (number, book['title'], book['author'], book['genres'])
        print(tw.dedent(book_message))
        if book['comments']:
            print('Комментарии:')
            for comment in book['comments']:
                print("-", comment)
        print()
    return
