import os
from builtins import input
import requests
import yaml
from src.interfaces.abc import AbstractBaseInterface

class Pocket(AbstractBaseInterface):
    def __init__(self):
        self._pocket_cfg = self.get_kenfile().get('pocket')
        self._api_url = 'https://getpocket.com/v3'

        if self._test_api_connection() != 200:
            self._configure_consumer_key()
            self._configure_access_token()
        else:
            print('API connection succeeded')

    # ---------------------------------------- #
    # -------- API KEY CONFIGURATIONS -------- #
    # ---------------------------------------- #
    def _configure_consumer_key(self):
        '''Checks if consumer key already exists in Kenfile.
        If not, provides directions for creation and adds to Kenfile.
        '''

        if self._pocket_cfg.get('consumer_key') is None:
            with open('src/templates/pocket/consumer_key_directions.txt', 'r') as f:
                print(f.read())

            consumer_key = input("\nPaste consumer key here and hit enter:\n> ")
            
            with open('Kenfile', 'w') as kenfile:
                self._kenfile['pocket']['consumer_key'] = consumer_key.strip()
                self._pocket_cfg['consumer_key'] = consumer_key.strip()
                yaml.dump(self._kenfile, kenfile, default_flow_style=False)
            print('Finished configuring consumer key\n')
        else:
            print('Consumer key already configured')
        return


    def _configure_access_token(self):
        '''Tests api connection with existing token
        If status is 200, then proceed. Otherwise, generate a new token.
        '''
        if self._test_api_connection() != 200:
            key = self._pocket_cfg.get('consumer_key')

            request_token = self._get_authorization_request_token()
            self._get_access_token(request_token)

            print('Finished configuring access token\n')
        else:
            print('Access token already configured')
        return

    # ---------------------------------------- #
    # -------- API CONNECTION HELPERS -------- #
    # ---------------------------------------- #
    def _test_api_connection(self):
        '''Tests api connection using provided consumer key and access token.
        Returns the status code
        '''
        key = self._pocket_cfg.get('consumer_key')
        token = self._pocket_cfg.get('access_token')
        payload = {'consumer_key': key, 
                   'access_token': token, 
                   'count':'1', 
                   'detailType':'complete'}

        url = f'{self._api_url}/get'
        status = requests.get(url, payload)
        return status.status_code


    def _get_authorization_request_token(self):
        '''Sends api request to generate the authorization request token
        '''
        key = self._pocket_cfg.get('consumer_key')
        req = requests.get('https://getpocket.com/v3/oauth/request', 
                            params={'consumer_key': key, 
                                    'redirect_uri': 'https://www.google.com'})
        
        request_token = req.content.decode('utf-8').split('=')[1]

        return request_token


    def _get_access_token(self, request_token):
        '''Generates access token upon user authorization and adds to
        the Kenfile.
        '''
        key = self._pocket_cfg.get('consumer_key')
        redirect_uri = 'https://giphy.com/gifs/zCME2Cd20Czvy/fullscreen'
        auth_url = 'https://getpocket.com/auth/authorize?' +\
                    f'request_token={request_token}&' +\
                    f'redirect_uri={redirect_uri}'

        with open('src/templates/pocket/access_token_directions.txt', 'r') as f:
            token_directions = f.read().replace('<url>', auth_url)
            print(token_directions)

        input('\nAfter completing authentication, press Enter to continue\n')

        auth = requests.get('https://getpocket.com/v3/oauth/authorize', 
                            params={'consumer_key': key, 
                                    'code': request_token})

        access_token = auth.content.decode('utf-8').split('&')[0].split('=')[1]

        with open('Kenfile', 'w') as kenfile:
            self._kenfile['pocket']['access_token'] = access_token.strip()
            self._pocket_cfg['access_token'] = access_token.strip()
            yaml.dump(self._kenfile, kenfile, default_flow_style=False)
        
        print('Access token generated and added to Kenfile')
        return

    # ---------------------------------------- #
    # ------- USER INTERFACE FUNCTIONS ------- #
    # ---------------------------------------- #
    def get_articles(self, count=10):
        print('\n')
        payload = {'consumer_key': self._pocket_cfg.get('consumer_key'), 
                   'access_token': self._pocket_cfg.get('access_token'), 
                   'count': count, 
                   'detailType': 'incomplete'}

        req = requests.get(f'{self._api_url}/get', payload).json()
        articles = req['list']
        for i,article in enumerate(articles):
            print(f"Article {i+1}: {articles[article]['resolved_title']}")
        print('\n')
    

    def add_article(self, url, title):
        payload = {
            'url': url,
            'title': title,
            'consumer_key': self._pocket_cfg.get('consumer_key'), 
            'access_token': self._pocket_cfg.get('access_token')}
        requests.post(f'{self._api_url}/add', payload)
        return


if __name__=='__main__':
    pkt = Pocket()
    pkt.get_articles(2)
    pkt.reset_kenfile()
    # url = 'https://www.ft.com/content/b2f861ad-74e7-4ce9-8449-f8bb22053596'
    # title = 'Global equities suffer worst week since March'
    # pkt.add_article(url, title)
