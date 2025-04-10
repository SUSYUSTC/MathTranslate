import json
import urllib.request


def get_latest_version():
    url = 'https://pypi.org/pypi/mathtranslate/json'

    with urllib.request.urlopen(url,timeout=15) as response:
        data = json.loads(response.read().decode('utf-8'))
        latest_version = data['info']['version']

    return latest_version
