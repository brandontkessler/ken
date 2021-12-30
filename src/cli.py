from collections import deque

from pocket import AutoPocket

from crawlers.guardian import guardian
from crawlers.vice import vice
from crawlers.chess import chess
from crawlers.economist import economist
from crawlers.vox import vox

pocket = AutoPocket()


def compile_articles(newssites, limit_per_site=10):
    compiled_articles = []
    if 'vox' in newssites: compiled_articles += vox(limit_per_site)
    if 'economist' in newssites: compiled_articles += economist(limit_per_site)
    if 'chess' in newssites: compiled_articles += chess(limit_per_site)
    if 'vice' in newssites: compiled_articles += vice(limit_per_site)
    if 'guardian' in newssites: compiled_articles += guardian(limit_per_site)
    return compiled_articles


def cli_exec(compiled_articles):
    user_add = ['y', 'yes', 'ya', 'yeah', 'ok']
    user_skip = ['n', 'no', 'nah', 'pass', 'skip']
    user_back = ['back', 'undo']
    user_quit = ['quit', 'exit']

    print('\nCompiling articles for AutoPocket\n')
    articles = deque(compiled_articles)
    print('-> DIRECTIONS <-')
    print('Each article will be displayed one by one.')
    print('Provide input in the command line and hit enter based on the following instructions:')
    print(f'* To add an article, provide: {user_add}')
    print(f'* To pass an on article, provide: {user_skip} or just hit Enter')
    print(f'* To go back on an article that was passed on, provide: {user_back}')
    print(f'* To quit the program: {user_quit}')
    print('\nReady? [Hit enter to continue]')
    input()
    print('######### STARTING AUTOPOCKET ##########\n')
    passed_articles = []

    while True:
        print('This is the last article') if len(articles) == 1 else print(f'There are {len(articles)} articles left.')

        article = articles.popleft()
        print(f'\n-> {article.source} -- {article.title}')
        decision = input('Do you want to add this to pocket?\n').lower()

        if decision in user_quit:
            print("EXITING PROGRAM")
            break
        elif decision in user_add:
            pocket.add_article(article.url, article.title)
            print('\n######### ADDED TO POCKET ##########\n')
        elif decision in user_skip or decision == '':
            print('\n######### SKIPPED ##########\n')
            passed_articles.append(article)
        elif decision in user_back:
            if len(passed_articles) > 0:
                print('\n######### BACK ##########\n')
                prior_article = passed_articles.pop()
                articles.appendleft(article)
                articles.appendleft(prior_article)
            else:
                print('\n######### NO ARTICLES TO GO BACK TO ##########\n')
                articles.appendleft(article)
        else:
            print("\nUnable to register command, try again:\n")
            articles.appendleft(article)

        if len(articles) == 0: 
            print("\n######### NO MORE ARTICLES ##########\n")
            print("-> Thanks for using AutoPocket <-\n\n")
            break

if __name__ == '__main__':
    newssites = [
        # 'vox',
        'economist',
        'guardian',
        # 'vice',
        'chess',
    ]
    articles = compile_articles(newssites, limit_per_site=20)
    cli_exec(articles)