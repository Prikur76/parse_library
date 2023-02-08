import os
import requests


def fetch_text_from_library(book_id):
    """ TODO """
    txt_url = 'https://tululu.org/txt.php'
    payload = {
        'id': book_id
    }
    response = requests.get(url=txt_url, params=payload)
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


def main():
    books_path = './books/'
    if not os.path.exists(books_path):
        os.makedirs(books_path)
    for book_id in range(1, 11):
        try:
            filename = os.path.join(books_path, f"id{book_id}.txt")
            response = fetch_text_from_library(book_id)
            if check_for_redirect(response):
                book_text = response.content
                download_book(filename, book_text)
        except requests.exceptions.HTTPError as err:
            print(f"book_id {book_id}: {err}")
    return


if __name__ == '__main__':
    main()
