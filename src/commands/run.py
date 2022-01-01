import os
import sys
from collections import deque
import click
from src.utils import config_funcs as cf
from src.commands.helpers.run.compile_articles import compile_articles
from src.commands.helpers.run.run_factory import run_factory
from src import interfaces as I


@click.command(no_args_is_help=False)
@click.option('--state-path', '-sp', 
              default=os.path.join(os.path.expanduser('~'), '.ken', 'state'))
def run(state_path):
    state = cf.get_state(state_path)

    interface_list = [k for k,v in state['interface'].items() if v is True]
    interfaces = {
        'pocket': I.Pocket()
    }
    # need to be able to dynamically add interfaces
    
    instructions = os.path.join('src', 'static', 'ken', 'instructions.txt')
    with open(instructions, 'r') as f:
        click.echo(f'\n{f.read()}')

    click.confirm('Hit enter to continue', default='Y', show_default=False)
    click.echo('\n-- Ken is Running --\n')

    articles = deque(compile_articles(state))
    skipped_articles = deque()

    while True:
        click.secho(f'\narticles remaining: {len(articles)}', nl=False, bold=True)
        article = articles.popleft()
        
        click.echo(f'\nfrom: {article.source}')
        click.echo(f'article: {article.title}')

        command = click.prompt('command')
        run_factory(interfaces, article, command, instructions, articles, skipped_articles)

        if len(articles) == 0: break
