import click

from src import commands as cmd

@click.group(chain=False)
@click.version_option()
def ken():
    pass

ken.add_command(cmd.subscribe)
ken.add_command(cmd.unsubscribe)

# @cli.command('sdist')
# def sdist():
#     click.echo('sdist called')


# @cli.command('bdist_wheel')
# def bdist_wheel():
#     click.echo('bdist_wheel called')

if __name__== '__main__':
    ken()

