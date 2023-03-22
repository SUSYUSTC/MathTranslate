default_engine = 'google'  # google or tencent
default_language_from = 'en'
default_language_to = 'zh-CN'

# Do not change the following unless you know what you are doing
# 请不要更改下面的代码，除非您理解自己在做什么

import os
from . import ROOT

if os.environ.get("TENCENTCLOUD_SECRET_ID") is not None:
    tencent_secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
elif os.path.exists(f'{ROOT}/TENCENT_ID'):
    tencent_secret_id = open(f'{ROOT}/TENCENT_ID').read().replace(' ', '').replace('\n', '')
else:
    tencent_secret_id = None

if os.environ.get("TENCENTCLOUD_SECRET_KEY") is not None:
    tencent_secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
elif os.path.exists(f'{ROOT}/TENCENT_KEY'):
    tencent_secret_key = open(f'{ROOT}/TENCENT_KEY').read().replace(' ', '').replace('\n', '')
else:
    tencent_secret_key = None

math_code = 'XMATHX'
