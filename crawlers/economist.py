import requests
from bs4 import BeautifulSoup
from .helpers import aggregate_articles


def economist(limit=10):
    url = 'https://www.economist.com'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    articles = soup.findAll('a', {'class': 'headline-link'})

    aggregate = aggregate_articles(articles, prepend_url=url)

    return aggregate[:limit]
