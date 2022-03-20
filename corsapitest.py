import requests

def check_user(user):
    """ Exchanges Auth code for user token
    """
    url = 'http://127.0.0.1:8000/api/data'
    data = {
        'user': user
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()

check_user("ericstinky")