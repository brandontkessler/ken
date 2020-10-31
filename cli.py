from collections import deque

import crawlers
from pocket import AutoPocket
from cl_formatting import Format

pocket = AutoPocket()


def compile_articles(newssites=['financial_times', 'guardian'], limit_per_site=10):
    compiled_articles = []
    if 'financial_times' in newssites: compiled_articles += crawlers.financial_times(limit_per_site)
    if 'guardian' in newssites: compiled_articles += crawlers.guardian(limit_per_site)
    return compiled_articles


def cli_exec(compiled_articles):
    print('\nCompiling articles for AutoPocket\n')
    articles = deque(compiled_articles)
    print(f'{Format.BOLD}{Format.BLUE}DIRECTIONS:{Format.END}')
    print('Each article will be displayed one by one.')
    print('Provide input in the command line and hit enter based on the following instructions:')
    print('* To pass an on article, provide: [n, no, nah, pass, skip]')
    print('* To go back on an article that was passed on, provide: [back]')
    print('* To add an article, provide any other input or no input at all.')
    print('\nReady? [Hit enter to continue]')
    input()
    print(f'{Format.BOLD}######### Starting AutoPocket ##########{Format.END}\n')
    passed_articles = []

    while True:
        if len(articles) == 1:
            print('This is the last article')
        else:
            print(f'There are {len(articles)} articles left.')

        article = articles.popleft()
        print(f'Next article: {Format.BOLD}{article.title}{Format.END}')
        decision = input('Do you want to add this to pocket?\n').lower()

        if decision in ['n', 'no', 'nah', 'pass', 'skip']:
            print(f'\n{Format.BOLD}RESPONSE: {Format.END}Passed on: {article.title}\n')
            passed_articles.append(article)
        elif decision in ['back', 'undo']:
            if len(passed_articles) > 0:
                print(f'\n{Format.BOLD}RESPONSE: {Format.END}Going to last skipped article.\n')
                prior_article = passed_articles.pop()
                articles.appendleft(article)
                articles.appendleft(prior_article)
            else:
                print(f'{Format.BOLD}RESPONSE: {Format.END}There are no articles to go back to.\n')
                articles.appendleft(article)
        else:
            pocket.add_article(article.url, article.title)
            print(f'\n{Format.BOLD}RESPONSE: {Format.END}Added to pocket\n')

        if len(articles) == 0: 
            print("All articles have been accounted for.\n")
            print("Thanks for using AutoPocket.\n\n")
            break

if __name__ == '__main__':
    newssites = [
        'guardian'
    ]
    articles = compile_articles(newssites, limit_per_site=10)
    cli_exec(articles)