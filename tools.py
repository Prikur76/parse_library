import json
import os
import textwrap as tw
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

import exceptions


def get_response(target_url):
    """Возвращает ответ на запрос либо возбуждает исключение"""
    response = requests.get(url=target_url)
    response.raise_for_status()
    if response.history:
        raise requests.exceptions.HTTPError('Request failed with: ',
                                            response.history)
    return response


def fetch_text_url(url, soup):
    """
    Возвращает ссылку для скачивания текста книги (при наличии)
    или возбуждает исключение TypeError
    """
    tag_href = soup.select_one('table.d_book a[href*="/txt.php?id="]')
    if tag_href is None:
        raise exceptions.MyCustomError('No txt tag')
    return urljoin(url, tag_href.get('href'))


def fetch_image_url_and_name(url, soup):
    """Возвращает ссылку для скачивания изображения и имя файла"""
    image = soup.select_one('div.bookimage img')
    if image is None:
        raise exceptions.MyCustomError('No image tag')
    image_url = urljoin(url, image.get('src'))
    image_name = image_url.split('/')[-1]
    return image_url, image_name


def fetch_title_and_author(soup):
    """Возвращает название книги и автора"""
    title_tag = soup.select_one('h1').text
    if title_tag is None:
        raise exceptions.MyCustomError('No title text')
    title, author = title_tag.split(' :: ')
    return title.strip(), author.strip()


def fetch_genres(soup):
    """Возвращает жанр книги или пустой список"""
    genres_tags = soup.select('span.d_book a')
    if genres_tags is None:
        raise exceptions.MyCustomError('No genres tag')
    genres = [genre.text for genre in genres_tags]
    return genres


def fetch_comments(soup):
    """Возвращает список комментариев или пустой список"""
    comments_tags = soup.select('div.texts span')
    if comments_tags is None:
        raise exceptions.MyCustomError('No comments tag')
    comments = [comment.text for comment in comments_tags]
    return comments


def parse_book_page(response):
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
        'book_url': response.url, 'text_url': text_url, 'image_url': image_url,
        'image_name': image_name, 'title': title, 'author': author,
        'genres': genres, 'book_name': book_name, 'comments': comments
    }
    return book


def download_content(content_url, file_name, folder):
    """Функция для скачивания файлов в заданную папку"""
    response = requests.get(url=content_url)
    response.raise_for_status()
    if response.history:
        raise requests.exceptions.HTTPError('Redirect: ', response.history)

    filepath = os.path.join(folder, file_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)


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


def download_books_to_file(books, folder_path):
    """Возвращает файл со списком книг в формате json"""
    collected_books = []
    for book in books:
        collected_books.append(
            {
                'title': book['title'],
                'author': book['author'],
                'img_src': f"images/{book['image_name']}",
                'book_path': f"books/{book['book_name']}",
                'comments': book['comments'],
                'genres': book['genres']
            }
        )
    filename = os.path.join(folder_path, 'books.json')
    with open(filename, 'w+', encoding='utf8') as file:
        json.dump(collected_books, file,
                  ensure_ascii=False, indent=4)


def get_last_page_number():
    """Возвращает номер последней страницы """
    sci_fi_url = 'https://tululu.org/l55/'
    response = get_response(sci_fi_url)
    soup = BeautifulSoup(response.text, 'lxml')
    last_page_number = int(soup.select('a.npage')[-1].text)
    if last_page_number is None:
        raise exceptions.MyCustomError("No 'last page' tag")
    return last_page_number


def fetch_books_urls_from_page(page_url):
    """Возвращает список ID книг на указанной странице"""
    response = get_response(page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    a_tags = soup.select('div.bookimage > a')
    if a_tags is None:
        raise exceptions.MyCustomError('No book url tag')
    page_books_urls = [urljoin(page_url, tag['href']) for tag in a_tags]
    return page_books_urls
