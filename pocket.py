from builtins import input
import requests
import json
import webbrowser


class AutoPocket:
    def __init__(self):
        self._url = 'https://getpocket.com/v3'

        with open('.\config.json') as f:
            keys = json.load(f)
            self._consumer_key = keys['CONSUMER_KEY']
            try:
                self._check_access_token = keys['ACCESS_TOKEN']
            except:
                self._check_access_token = None


        self._status = self._test_connection()
        if self._status == 200:
            print('Pocket is already configured.\n')
            self._access_token = self._check_access_token
        else: 
            self._request_token = self._get_token()
            self._auth_url = f'https://getpocket.com/auth/authorize?request_token={self._request_token}&redirect_uri=https://google.com'
            self._access_token = self._user_auth()
        

        self._payload = {
            "consumer_key": self._consumer_key, 
            "access_token": self._access_token
        }

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
        print('A browser should have opened to the auth URL. If not, open a browser and paste the below link in the URL:')
        print(self._auth_url)
        print('Authenticate the application. Once redirected to google, return to the CLI and click any key.')

        webbrowser.open_new_tab(self._auth_url)
        input()

        payload = {"consumer_key":self._consumer_key, "code":self._request_token}
        auth = requests.get('https://getpocket.com/v3/oauth/authorize', params=payload)
        access_token = auth.content.decode('utf-8').split('&')[0].split('=')[1]

        with open('.\config.json', 'r') as f:
            keys = json.load(f)
            keys['ACCESS_TOKEN'] = access_token
        
        with open('.\config.json', 'w') as f:
            json.dump(keys, f, indent=4)

        print(f'Pocket is now configured.\n')
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