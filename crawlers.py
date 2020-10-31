import requests
from bs4 import BeautifulSoup
from collections import namedtuple

ArticleRecord = namedtuple('ArticleRecord', 'title, url')

def financial_times(limit=10):
    """Requires premium membership
    """
    url = 'https://www.ft.com'
    financial_times = requests.get(url)
    soup = BeautifulSoup(financial_times.content, 'html.parser')
    headlines = soup.findAll("a", {"class": "js-teaser-heading-link"}, limit=limit)

    articles = []

    for headline in headlines:
        article = ArticleRecord(headline.get_text(), f"{url}{headline.get('href')}")
        articles.append(article)
    
    return articles


def guardian(limit=10):
    url = 'https://www.theguardian.com/us'
    guardian = requests.get(url)
    soup = BeautifulSoup(guardian.content, 'html.parser')
    headlines = soup.findAll("a", {"data-link-name": "article"}, limit=limit)
    
    articles = []

    for headline in headlines:
        articles.append(ArticleRecord(headline.find('span', {'class': 'js-headline-text'}).get_text(), f"{url}{headline.get('href')}"))
    
    return articles
