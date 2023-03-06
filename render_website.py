import json
# from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server

from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload():
    """ """
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    with open("books.json", encoding='utf-8', errors='ignore') as file:
        books = json.load(file, strict=False)

    template = env.get_template('template.html')
    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as index_html:
        index_html.write(rendered_page)


def rebuild():
    on_reload()
    print("Site rebuilt")

rebuild()
server = Server()
server.watch('template.html', rebuild)
server.serve(root='.')

# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()
