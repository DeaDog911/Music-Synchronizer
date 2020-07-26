import requests


def make_request(url):
    response = requests.get(url)
    return response
