from src import crawlers as crwl\

def compile_articles(state):
    subscriptions = [k for k,v in state.get('subscriptions').items() if v==True]
    limit = state['settings']['articles_per_site_limit']

    compiled_articles = []

    if 'vox' in subscriptions: compiled_articles += crwl.vox(limit)
    if 'economist' in subscriptions: compiled_articles += crwl.economist(limit)
    if 'chess' in subscriptions: compiled_articles += crwl.chess(limit)
    if 'vice' in subscriptions: compiled_articles += crwl.vice(limit)
    if 'guardian' in subscriptions: compiled_articles += crwl.guardian(limit)
    return compiled_articles
