import os
import sys
from collections import deque
import click
from src.helpers import config_funcs as cf
from src.commands.helpers import compile_articles

@click.command(no_args_is_help=False)
@click.option('--state-path', '-sp', 
              default=os.path.join(os.path.expanduser('~'), '.ken', 'state'))
def run(state_path):
    state = cf.get_state(state_path)
    
    instructions = os.path.join('src', 'templates', 'ken', 'instructions.txt')
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
        run_factory(command, article, instructions)

        if len(articles) == 0: break


def run_factory(command, article, instructions):
    if command == 'help':
        click.echo('\n')
        with open(instructions, 'r') as f:
            for line in f:
                if line[0] == '-' or 'commands' in line:
                    click.echo(line, nl=False)
        click.echo(f'\nfrom: {article.source}')
        click.echo(f'article: {article.title}')
        command = click.prompt('command')
        return run_factory(command, article, instructions)

    elif command == 'quit':
        sys.exit('Aborted!')
    
    elif command == 'add':
        pass
    
    elif command == 'skip':
        pass
    
    elif command == 'back':
        pass
    
    else:
        click.echo('\nunrecognized command - select from the following', nl=False)
        return run_factory('help', article, instructions)



# while True:
#     print('This is the last article') if len(articles) == 1 else print(f'There are {len(articles)} articles left.')

#     article = articles.popleft()
#     print(f'\n-> {article.source} -- {article.title}')
#     decision = input('Do you want to add this to pocket?\n').lower()

#     if decision in user_quit:
#         print("EXITING PROGRAM")
#         break
#     elif decision in user_add:
#         pocket.add_article(article.url, article.title)
#         print('\n######### ADDED TO POCKET ##########\n')
#     elif decision in user_skip or decision == '':
#         print('\n######### SKIPPED ##########\n')
#         passed_articles.append(article)
#     elif decision in user_back:
#         if len(passed_articles) > 0:
#             print('\n######### BACK ##########\n')
#             prior_article = passed_articles.pop()
#             articles.appendleft(article)
#             articles.appendleft(prior_article)
#         else:
#             print('\n######### NO ARTICLES TO GO BACK TO ##########\n')
#             articles.appendleft(article)
#     else:
#         print("\nUnable to register command, try again:\n")
#         articles.appendleft(article)

#     if len(articles) == 0: 
#         print("\n######### NO MORE ARTICLES ##########\n")
#         print("-> Thanks for using AutoPocket <-\n\n")
#         break

