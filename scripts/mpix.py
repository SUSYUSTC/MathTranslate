#!/usr/bin/env python
import base64
import requests
import json


def get_result(file_path):
    image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, "rb").read()).decode()
    r = requests.post("https://api.mathpix.com/v3/text",
        data=json.dumps({'src': image_uri}),
        headers={"app_id": "YOUR_APP_ID", "app_key": "YOU_APP_KEY",
                "Content-type": "application/json"})
    result = json.loads(r.text)
    return result


if __name__ == '__main__':
    import sys
    file_path = sys.argv[1]
    result = get_result(file_path)
    print(result['text'])
