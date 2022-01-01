import os
import sys
from collections import deque
import click
from src.utils import config_funcs as cf
from src.commands.helpers import compile_articles

@click.command(no_args_is_help=False)
@click.option('--state-path', '-sp', 
              default=os.path.join(os.path.expanduser('~'), '.ken', 'state'))
def run(state_path):
    state = cf.get_state(state_path)

    interfaces = [k for k,v in state['interface'].items() if v is True]
    
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


def run_factory(interfaces, article, command, instructions, articles, skipped_articles):
    if command == 'help':
        click.echo('\n')
        with open(instructions, 'r') as f:
            for line in f:
                if line[0] == '-' or 'commands' in line:
                    click.echo(line, nl=False)
        click.echo(f'\nfrom: {article.source}')
        click.echo(f'article: {article.title}')
        command = click.prompt('command')
        run_factory(interfaces, article, command, instructions, articles, skipped_articles)

    elif command == 'quit':
        sys.exit('Aborted!')
    
    elif command == 'add':
        for interface in interfaces:
            interface.add_article(article.url, article.title)
        click.echo('added')

    elif command == 'skip':
        skipped_articles.append(article)
        click.echo('skipped')
    
    elif command == 'back':
        if len(skipped_articles) > 0:
            prev_article = skipped_articles.pop()
            articles.appendleft(article)
            articles.appendleft(prev_article)
        else:
            articles.appendleft(article)
            click.echo('no previous articles')
    
    else:
        click.echo('\nunrecognized command - select from the following', nl=False)
        run_factory(interfaces, article, 'help', instructions, articles, skipped_articles)

    return