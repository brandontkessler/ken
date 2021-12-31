import click
from src.helpers import config_funcs as cf

def list_subscriptions(list_):
    if list_ is True:
        click.echo(click.style('\nsubscription list\n', bold=True), nl=False)
        click.echo('--------------------')
        for k,v in cf.get_state().get('subscriptions').items():
            if v == True:
                click.echo(k)
        click.echo('--------------------\n', nl=True)