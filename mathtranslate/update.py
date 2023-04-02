import requests


def get_latest_version():
    response = requests.get('https://pypi.org/pypi/mathtranslate/json')
    latest_version = response.json()['info']['version']
    return latest_version
