import requests
import json

url = "https://api.senuto.com//api/users/token.json"


def get_token():
    login_data = {'email': 'monitoring@vestigio.pl', 'password': '1nj14b24141$!$!'}
    r = requests.post(url, data=login_data)
    # loading json users data for token
    user_data = json.loads(r.text)
    # getting token
    token = user_data['data']['token']
    return token
