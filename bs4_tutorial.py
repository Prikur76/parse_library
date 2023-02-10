import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()
# print(response.text)

soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())
# print(soup.find('h1'))

img_tag = soup.find('img', class_='attachment-post-image')
# print(img_tag)

img_link = soup.find('img', class_='attachment-post-image')['src']
print(img_link)

title_tag = soup.find('main').find('header').find('h1')
# print(title_tag)

title_text = title_tag.text
print(title_text)

text_tags = soup.find('main').find('div', class_='entry-content').find_all('p')
# print(text_tags)
text = []
for p in text_tags:
    text.append(p.text)
print(''.join(text))