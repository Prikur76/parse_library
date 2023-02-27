import argparse
import logging
import os
import textwrap as tw
import time
from urllib.parse import urljoin
import re

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

logger = logging.getLogger(__name__)


def has_tag_title(tag):
    return tag.has_attr('title') and tag.has_attr('href')

def main():
    """TODO"""

    return


if __name__ == '__main__':
    # main()
    # base_url = 'https://tululu.org/fantastic/'
    science_fiction_url = 'https://tululu.org/l55/'
    response = requests.get(url=science_fiction_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    hrefs = []
    for tag in soup.find('div', id='content')\
            .find_all('a', title=re.compile('скачать')):
        hrefs.append(tag.get('href'))

    print(hrefs)


    # categories_tags = soup.find('div', class_='lbt').find_all('a')
    # categories = []
    # for category in categories_tags:
    #     categories.append(category.get('href'))
    # print(categories)

