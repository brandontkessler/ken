import requests
from bs4 import BeautifulSoup
from .helpers import aggregate_articles


def vox(limit=10):
    url = 'https://www.vox.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')


    articles = soup.findAll('a', {'data-chorus-optimize-field': 'hed'})

    aggregate = aggregate_articles(articles)

    return aggregate[:limit]
