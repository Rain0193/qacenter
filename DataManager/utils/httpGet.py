import requests

def httpGet(url):
    result = requests.get(url).text
    return result