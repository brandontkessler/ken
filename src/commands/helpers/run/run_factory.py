import click
import sys

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
        for interface in interfaces.keys():
            interfaces[interface].add_article(article.url, article.title)
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