import os
import shutil
import yaml


def get_kenfig():
    with open('Kenfig', 'r') as configuration:
        return yaml.safe_load(configuration)


def reset_kenfig():
    shutil.copyfile('templates/kenfile.yaml', 'Kenfig')


def set_state(path=os.path.expanduser('~')):
    if not os.path.exists(os.path.join(path, '.ken')):
        os.mkdir(os.path.join(path, '.ken'))
    
    with open(os.path.join(path, '.ken', 'state'), 'w+') as f:
        yaml.dump(get_kenfig(), f)


def get_state(path=os.path.expanduser('~')):
    with open(os.path.join(path, '.ken', 'state'), 'r') as f:
        return yaml.safe_load(f)

def edit_state(section, key, value, path=os.path.expanduser('~')):
    state = get_state()
    state[section][key] = value

    with open(os.path.join(path, '.ken', 'state'), 'w') as f:
        yaml.dump(state, f, default_flow_style=False)


def coalesce_state_with_kenfig(path=os.path.expanduser('~')):
    new_opts = get_kenfig()
    state = get_state()

    for section in new_opts.keys():
        if section not in state.keys():
            state[section] = {}
        for k,v in new_opts[section].items():
            if v is not None:
                state[section][k] = v
    
    with open(os.path.join(path, '.ken', 'state'), 'w') as f:
        yaml.dump(state, f, default_flow_style=False)

def get_subscription_options():
    with open(os.path.join('templates/kenfile.yaml'), 'r') as template:
        return yaml.safe_load(template)['subscriptions'].keys()

if __name__=='__main__':
    root = os.path.expanduser('~')

    if os.path.exists(os.path.join(root, '.ken', 'state')):
        coalesce_state_with_kenfig()
    else:
        set_state()
    
    reset_kenfig()
