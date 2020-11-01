import requests
from bs4 import BeautifulSoup
from .helpers import aggregate_articles

def guardian(limit=10):
    url = 'https://www.theguardian.com/us'
    guardian = requests.get(url)
    soup = BeautifulSoup(guardian.content, 'html.parser')
    headlines = soup.find('div', {'data-title': 'Headlines'})

    # Get all articles from the headlines, filtering out any articles that have 
    #   a class that contains any of the strings in the class_filters list.
    class_filters = ['fc-sublink__link', 'faux']
    headline_articles = [
        headline for headline in headlines.findAll(
            "a", {"data-link-name": "article"}
        ) if not any([
            filter in h_class for h_class in headline['class'] for filter in class_filters
        ])
    ]

    articles = aggregate_articles(headline_articles)
    
    return articles[:limit]