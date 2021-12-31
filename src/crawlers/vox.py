import requests
from bs4 import BeautifulSoup
from src.crawlers.helpers.aggregate_articles import aggregate_articles


def vox(limit=10):
    src = 'Vox'
    url = 'https://www.vox.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')


    articles = soup.findAll('a', {'data-chorus-optimize-field': 'hed'})

    aggregate = aggregate_articles(articles, source=src)

    return aggregate[:limit]
