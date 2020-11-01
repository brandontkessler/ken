from collections import namedtuple

def aggregate_articles(soup_articles, prepend_url=None):
    """soup_articles should be a list of A tags
    
    Use prepend_url to include a portion of url 
        before what comes in from the parse.
    """

    ArticleRecord = namedtuple('ArticleRecord', 'title, url')
    articles = []

    for article in soup_articles:
        article_title = article.get_text().strip()
        article_url = f"{prepend_url}{article.get('href')}" if prepend_url else f"{article.get('href')}"
        
        articles.append(ArticleRecord(article_title, article_url))
    
    return articles