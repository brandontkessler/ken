import os
from builtins import input
import requests
import json
import webbrowser
import time

from cl_formatting import Format

class AutoPocket:
    def __init__(self):
        self._url = 'https://getpocket.com/v3'
        self._consumer_key, self._check_access_token = self._config()

        self._status = self._test_connection()
        if self._status == 200:
            print('Pocket is already configured.')
            time.sleep(1)
            self._access_token = self._check_access_token
        else: 
            self._request_token = self._get_token()
            self._auth_url = f'https://getpocket.com/auth/authorize?request_token={self._request_token}&redirect_uri=https://google.com'
            self._access_token = self._user_auth()
        

        self._payload = {
            "consumer_key": self._consumer_key, 
            "access_token": self._access_token
        }
    
    def _config(self):
        missing_consumer_key = False
        configs_exist = os.path.isfile('./config.json')
        if not configs_exist: print("config.json file is not detected.\n")

        if configs_exist:
            with open('config.json') as f:
                try:
                    json.load(f)['CONSUMER_KEY']
                except Exception:
                    missing_consumer_key = True
                    print("config.json file detected, but CONSUMER_KEY is not provided.\n")

        if not configs_exist or missing_consumer_key:
            time.sleep(2)
            print("A browser will open with the following URL:\n-> https://getpocket.com/developer/\n")
            time.sleep(2)
            print("If it does not, copy the URL and paste it into a browser, then follow the instructions below...\n")
            time.sleep(2)
            webbrowser.open_new_tab('https://getpocket.com/developer/')
            print(f"{Format.BOLD}DIRECTIONS: {Format.END}")
            print("* Click 'CREATE NEW APP'")
            print("* Name your application anything you want (mine is named AutoPocket)")
            print("* Enter anything for the description")
            print("* For permissions, check: Add, Modify, and Retrieve")
            print("* For Platforms, check: Desktop (other)")
            print("* Check the box for 'I accept the Terms of Service'")
            print("* Click 'CREATE APPLICATION'")
            print("* Provide the consumer key to continue.\n")
            time.sleep(1)
            key = input("Paste consumer key here and hit enter:\n> ")
            init_config_data = {
                'CONSUMER_KEY': key.strip()
            }
            
            with open('./config.json', 'w') as f:
                json.dump(init_config_data, f, indent=4)

        with open('./config.json') as f:
            keys = json.load(f)
            consumer_key = keys['CONSUMER_KEY']
            try:
                check_access_token = keys['ACCESS_TOKEN']
            except:
                check_access_token = None
        
        return consumer_key, check_access_token

    def _get_token(self):
        payload_auth_token = {'consumer_key': self._consumer_key, 'redirect_uri': 'https://google.com'}
        token_req = requests.get('https://getpocket.com/v3/oauth/request', params=payload_auth_token)
        code = token_req.content.decode('utf-8').split('=')[1]
        return code
    
    def _test_connection(self):
        payload = {'consumer_key': self._consumer_key, 'access_token': self._check_access_token, 'count':'1', 'detailType':'complete'}
        url = f'{self._url}/get'
        status = requests.get(url, payload)
        return status.status_code

    def _user_auth(self):
        time.sleep(2)
        print('\nA browser will open to the auth URL. If not, open a browser and follow the below url:')
        print(f'-> {self._auth_url}')
        print('\nAuthenticate the application. Once redirected to google you have been authenticated.')
        time.sleep(2)
        webbrowser.open_new_tab(self._auth_url)
        input('\nAfter completing authentication, press Enter to continue\n> ')

        payload = {"consumer_key":self._consumer_key, "code":self._request_token}
        auth = requests.get('https://getpocket.com/v3/oauth/authorize', params=payload)
        access_token = auth.content.decode('utf-8').split('&')[0].split('=')[1]

        with open('.\config.json', 'r') as f:
            keys = json.load(f)
            keys['ACCESS_TOKEN'] = access_token
        
        with open('.\config.json', 'w') as f:
            json.dump(keys, f, indent=4)

        print(f'\n{Format.BOLD}Pocket is now configured.{Format.END}\n')
        return access_token

    def get_articles(self, count=10):
        print('\n')
        payload = {**self._payload, "count":count, "detailType":"incomplete"}
        req = requests.get(f'{self._url}/get', payload).json()
        articles = req['list']
        for i,article in enumerate(articles):
            print(f"Article {i+1}: {articles[article]['resolved_title']}")
        print('\n')
    
    def add_article(self, url, title):
        payload = {
            "url": url,
            "title": title,
            **self._payload}
        req = requests.post(f'{self._url}/add', payload)
        print('Article added to pocket.')

if __name__=='__main__':
    pkt = AutoPocket()
    pkt.get_articles(3)
    # url = 'https://www.ft.com/content/b2f861ad-74e7-4ce9-8449-f8bb22053596'
    # title = 'Global equities suffer worst week since March'
    # pkt.add_article(url, title)