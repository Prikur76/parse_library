import os
import requests


def fetch_text_from_library(id):
    """ TODO """
    txt_url = 'https://tululu.org/txt.php'
    payload = {
        'id': id
    }
    response = requests.get(url=txt_url, params=payload)  # verify=False
    response.raise_for_status()
    return response.content


def download_book(filename, book_text):
    """Записываем файл"""
    with open(filename, 'wb') as file:
        file.write(book_text)


def main():


    books_path = './books/'
    if not os.path.exists(books_path):
        os.makedirs(books_path)

    for txt_id in range(1, 11):
        book_text = fetch_text_from_library(txt_id)
        filename = os.path.join(books_path, f"id{txt_id}.txt")
        download_book(filename, book_text)
    return


if __name__ == '__main__':
    main()
