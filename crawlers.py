import requests
from bs4 import BeautifulSoup
from collections import namedtuple

ArticleRecord = namedtuple('ArticleRecord', 'title, url')

# INCOMPLETE
# def financial_times(limit=10):
#     """Requires premium membership
#     """
#     url = 'https://www.ft.com'
#     financial_times = requests.get(url)
#     soup = BeautifulSoup(financial_times.content, 'html.parser')
#     headlines = soup.findAll("a", {"class": "js-teaser-heading-link"}, limit=limit)

#     articles = []

#     for headline in headlines:
#         article = ArticleRecord(headline.get_text(), f"{url}{headline.get('href')}")
#         articles.append(article)
    
#     return articles


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

    articles = []

    for article in headline_articles:
        article_title = article.get_text()
        article_url = f"{article.get('href')}"
        
        articles.append(ArticleRecord(article_title, article_url))
    
    return articles[:limit]


if __name__=='__main__':
    guardian()