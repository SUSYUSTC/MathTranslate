default_engine = 'google'  # google or tencent
default_language_from = 'en'
default_language_to = 'zh-CN'

tencent_secret_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
tencent_secret_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Do not change the following unless you know what you are doing
# 请不要更改下面的代码，除非您理解自己在做什么

import os
if os.environ.get("TENCENTCLOUD_SECRET_ID") is not None:
    tencent_secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
if os.environ.get("TENCENTCLOUD_SECRET_KEY") is not None:
    tencent_secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

math_code = 'XMATHX'
