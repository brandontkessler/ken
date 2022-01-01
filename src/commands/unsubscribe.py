import click
from src.utils import config_funcs as cf
from src.commands.helpers import list_subscriptions

@click.command(no_args_is_help=True)
@click.option('--all', '-a', 'all_', is_flag=True)
@click.option('--to', '-t', type=click.Choice(cf.get_subscription_options()),
              multiple=True)
@click.option('--list', '-l', 'list_', is_flag=True)
def unsubscribe(all_, to, list_):
    if all_ is True:
        for sub in cf.get_state().get('subscriptions').keys():
            cf.edit_state('subscriptions', sub, False)

    if len(to) > 0:
        for opt in to:
            cf.edit_state('subscriptions', opt, False)

    list_subscriptions(list_)

if __name__=='__main__':
    unsubscribe()