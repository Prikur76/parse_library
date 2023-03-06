import json
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    """ """
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    with open("books.json", encoding='utf-8', errors='ignore') as file:
        deserialized_file = json.load(file, strict=False)
        chunks = list(chunked(deserialized_file, 2))

    template = env.get_template('template.html')
    rendered_page = template.render(chunks=chunks)
    with open('index.html', 'w', encoding="utf8") as index_html:
        index_html.write(rendered_page)


def rebuild():
    on_reload()
    print("Site rebuilt")


rebuild()
server = Server()
server.watch('template.html', rebuild)
server.serve(root='.')
