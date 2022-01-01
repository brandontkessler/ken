import os
import click
from src.utils import config_funcs as cf
from src import crawlers as crwl

def list_subscriptions(list_):
    if list_ is True:
        click.secho('\nsubscription list\n', bold=True, nl=False)
        click.echo('--------------------')
        for k,v in cf.get_state().get('subscriptions').items():
            if v == True:
                click.echo(k)
        click.echo('--------------------\n', nl=True)


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

