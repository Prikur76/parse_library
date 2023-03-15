import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload(books_source='books.json'):
    """Возвращает папку html_pages с файлами html"""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    with open(books_source, encoding='utf-8', errors='ignore') as file:
        books_descriptions = json.load(file, strict=False)

    cards_count_on_page = 20
    pagination_chunks = list(chunked(books_descriptions,
                                     cards_count_on_page))

    pages_count = len(pagination_chunks)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    pages_path = os.path.join(dir_path, 'html_pages')
    os.makedirs(pages_path, exist_ok=True)

    template = env.get_template('templates/template.html')
    for page_number, page in enumerate(pagination_chunks, start=1):
        index_html_path = f'{pages_path}/index{page_number}.html'
        books_pages = [
            {
                'number': page_number,
                'content': page,
                'path': index_html_path,
                'count': pages_count
            }
        ]
        rendered_page = template.render(books_pages=books_pages)
        with open(index_html_path, 'w', encoding='utf8') as index_html:
            index_html.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(
        description="""\
            Запуск отладочного веб-сервера библиотеки
            """
    )
    parser.add_argument('-bs', '--books_source', default='books.json',
                        help='Ввести путь к файлу с описанием книг')
    args = parser.parse_args()
    books_source = args.books_source

    on_reload(books_source)

    server = Server()
    server.watch('../templates/template.html', on_reload)
    server.serve(root='.', default_filename='index.html')


if __name__ == '__main__':
    main()
