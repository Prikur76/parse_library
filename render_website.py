import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    """Возвращает папку pages с файлами html"""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    with open("books.json", encoding='utf-8', errors='ignore') as file:
        deserialized_file = json.load(file, strict=False)
        pages = list(chunked(deserialized_file, 20))
        pages_count = len(pages)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    pages_path = os.path.join(dir_path, 'pages')
    os.makedirs(pages_path, exist_ok=True)

    template = env.get_template('template.html')
    for page_number, page in enumerate(pages, start=1):
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
        with open(index_html_path, 'w', encoding="utf8") as index_html:
            index_html.write(rendered_page)


def rebuild():
    on_reload()
    print("Site rebuilt")


rebuild()
server = Server()
server.watch('template.html', rebuild)
server.serve(root='.', default_filename='./pages/index1.html')
