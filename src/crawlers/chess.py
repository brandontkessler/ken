import requests
from bs4 import BeautifulSoup
from .helpers import aggregate_articles


def chess(limit=10):
    src = 'Chess.com'
    url = 'https://www.chess.com/news'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    articles = soup.findAll('article', {'class': 'post-preview-component'})

    stop_index = None

    for i,article in enumerate(articles):
        posted = article.find('span', {'class': 'post-preview-meta-content'}).select('span:first-child')[0].text
        if 'day' in posted:
            stop_index = i
            break
    
    # Stop index will be an integer if there is an article posted a day or more ago
    #   otherwise stop index will be None indicating that all articles were posted today
    #   meaning don't filter any articles on the page.
    filtered_articles = articles[:stop_index] if isinstance(stop_index, int) else articles
    article_tags = [a.find('a', {'class': 'post-preview-title'}) for a in filtered_articles]

    aggregate = aggregate_articles(article_tags, source=src)

    return aggregate[:limit]
