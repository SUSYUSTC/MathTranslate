import os
from . import ROOT


def read_variable(path, default):
    if os.path.exists(f'{ROOT}/{path}'):
        return open(f'{ROOT}/{path}').read().replace(' ', '').replace('\n', '')
    else:
        return default


def set_variable(path, default):
    var = input().replace(' ', '').replace('\n', '')
    if var != '':
        return print(var, file=open(f'{ROOT}/{path}', 'w'))
    else:
        return default


def reread():
    global default_engine, default_language_from, default_language_to, tencent_secret_id, tencent_secret_key
    default_engine = read_variable(default_engine_path, default_engine_default)
    default_language_from = read_variable(default_language_from_path, default_language_from_default)
    default_language_to = read_variable(default_language_to_path, default_language_to_default)
    tencent_secret_id = read_variable(tencent_secret_id_path, tencent_secret_id_default)
    tencent_secret_key = read_variable(tencent_secret_key_path, tencent_secret_key_default)


default_engine_path = 'DEFAULT_ENGINE'
default_language_from_path = 'DEFAULT_LANGUAGE_FROM'
default_language_to_path = 'DEFAULT_LANGUAGE_TO'
tencent_secret_id_path = 'TENCENT_ID'
tencent_secret_key_path = 'TENCENT_KEY'

default_engine_default = 'google'
default_language_from_default = 'en'
default_language_to_default = 'zh-CN'
tencent_secret_id_default = None
tencent_secret_key_default = None

default_engine = read_variable(default_engine_path, default_engine_default)
default_language_from = read_variable(default_language_from_path, default_language_from_default)
default_language_to = read_variable(default_language_to_path, default_language_to_default)
tencent_secret_id = read_variable(tencent_secret_id_path, tencent_secret_id_default)
tencent_secret_key = read_variable(tencent_secret_key_path, tencent_secret_key_default)

math_code = 'XMATHX'
