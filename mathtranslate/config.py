default_engine = 'google'  # google or tencent

google_language_from = 'en'
google_language_to = 'zh-CN'

tencent_language_from = 'en'
tencent_language_to = 'zh'
tencent_secret_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
tencent_secret_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

default_languages = {
    'google': {
        'from': google_language_from,
        'to': google_language_to,
    },
    'tencent': {
        'from': tencent_language_from,
        'to': tencent_language_to,
    },
}

default_language_from = tencent_language_from
default_language_to = tencent_language_to
