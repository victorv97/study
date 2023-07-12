import os
import requests
from bs4 import BeautifulSoup
import re
import string


PUNCTUATION = ''.join(['[', string.punctuation, ']'])

URL = 'https://www.nature.com'
ARTICLES_HREF = '/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={}'.format

ARTICLE_TAG = 'article'

ARTICLE_TYPE_TAG = 'span'
ARTICLE_TYPE_ATTR = {'class': 'c-meta__type'}

ARTICLE_TITLE_TAG = 'h3'
ARTICLE_TITLE_ATTR = {'class': 'c-card__title'}


def get_response_content(user_url):
    response = requests.get(user_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response.status_code != 200:
        print(f'The URL returned {response.status_code}!')
        return

    return response.content


def get_soup(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def save_content(name, content):
    with open(f'{name}.txt', 'w', encoding='utf8') as file:
        file.write(content)
    print(f'Content {name}.txt saved.')


def get_articles(page_number, article_type):
    page_dir = f'Page_{page_number}'
    os.makedirs(page_dir, exist_ok=True)

    content = get_response_content(''.join([URL, ARTICLES_HREF(page_number)]))
    if not content:
        print(f'Got no content on page {page_number}')
        return
    soup = get_soup(content)

    titles = []
    articles = soup.find_all(ARTICLE_TAG)
    for article in articles:
        a_type = article.find(ARTICLE_TYPE_TAG, ARTICLE_TYPE_ATTR).text
        if a_type == article_type:
            article_title = article.find(ARTICLE_TITLE_TAG, ARTICLE_TITLE_ATTR)
            article_href = article_title.find('a', href=True)['href']
            content = get_response_content(''.join([URL, article_href]))
            if not content:
                continue
            article_soup = get_soup(content)
            article_body = article_soup.find('p', {'class': 'article__teaser'})
            article_title_name = re.sub(PUNCTUATION, '', article_title.text.strip())
            article_title_name = re.sub(r'\s', '_', article_title_name)

            save_content(os.path.join(page_dir, article_title_name), article_body.text)
            titles.append(f'{article_title_name}.txt')
    return titles


def main():
    number_of_pages = int(input('Enter number of pages:'))
    article_type = input('Enter desired articles type:')
    for n in range(1, number_of_pages + 1):
        titles = get_articles(n, article_type)
    print('Saved all articles.')


if __name__ == '__main__':
    main()
