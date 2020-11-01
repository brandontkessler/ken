from collections import deque

from pocket import AutoPocket

from crawlers.guardian import guardian
from crawlers.vice import vice
from crawlers.chess import chess

pocket = AutoPocket()


def compile_articles(newssites, limit_per_site=10):
    compiled_articles = []
    if 'chess' in newssites: compiled_articles += chess(limit_per_site)
    if 'vice' in newssites: compiled_articles += vice(limit_per_site)
    if 'guardian' in newssites: compiled_articles += guardian(limit_per_site)
    return compiled_articles


def cli_exec(compiled_articles):
    user_skip = ['n', 'no', 'nah', 'pass', 'skip']
    user_back = ['back', 'undo']

    print('\nCompiling articles for AutoPocket\n')
    articles = deque(compiled_articles)
    print('-> DIRECTIONS <-')
    print('Each article will be displayed one by one.')
    print('Provide input in the command line and hit enter based on the following instructions:')
    print(f'* To pass an on article, provide: {user_skip}')
    print(f'* To go back on an article that was passed on, provide: {user_back}')
    print('* To add an article, provide any other input or no input at all.')
    print('\nReady? [Hit enter to continue]')
    input()
    print('######### STARTING AUTOPOCKET ##########\n')
    passed_articles = []

    while True:
        if len(articles) == 1:
            print('This is the last article')
        else:
            print(f'There are {len(articles)} articles left.')

        article = articles.popleft()
        print(f'\n-> {article.title}')
        decision = input('Do you want to add this to pocket?\n').lower()

        if decision in user_skip:
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
            pocket.add_article(article.url, article.title)
            print('\n######### ADDED TO POCKET ##########\n')

        if len(articles) == 0: 
            print("\n######### NO MORE ARTICLES ##########\n")
            print("-> Thanks for using AutoPocket <-\n\n")
            break

if __name__ == '__main__':
    newssites = [
        'guardian',
        'vice',
        'chess'
    ]
    articles = compile_articles(newssites, limit_per_site=10)
    cli_exec(articles)