import requests
from bs4 import BeautifulSoup
from .helpers import aggregate_articles


def vice(limit=10):
    url = 'https://www.vice.com/en'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')


    articles = soup.findAll('a', {'class': 'vice-card-hed__link'})

    aggregate = aggregate_articles(articles, prepend_url='https://www.vice.com')

    return aggregate[:limit]
