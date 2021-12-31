import requests
from bs4 import BeautifulSoup
from src.crawlers.helpers.aggregate_articles import aggregate_articles


def economist(limit=10):
    src = 'Economist'
    url = 'https://www.economist.com'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    articles = soup.findAll('a', {'class': 'headline-link'})

    aggregate = aggregate_articles(articles, source=src, prepend_url=url)

    return aggregate[:limit]
