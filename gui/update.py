import requests
import zipfile
import os
import platform


def update_package(os_name):
    url = f'https://github.com/SUSYUSTC/MathTranslate/releases/latest/download/MathTranslate_{os_name}.zip'
    print(f'Downloading {url}')
    zippath = f'./MathTranslate_{os_name}.zip'
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        print("Cannot download, maybe due to network issues")
        return
    open(zippath, 'wb').write(r.content)

    with zipfile.ZipFile(zippath, 'r') as zip_ref:
        zip_ref.extractall('MathTranslate', members=filter(lambda x: x.filename[0:6] != 'update', zip_ref.infolist()))
    os.remove(zippath)


if __name__ == '__main__':
    os_names = {'Windows': 'Windows', 'Linux': 'Linux', 'Darwin': 'MacOS'}
    raw_name = platform.system()
    os_name = os_names[raw_name]
    update_package(os_name)
    input('Press Enter to exit')
