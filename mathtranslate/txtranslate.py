from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client
from .config import tencent_secret_id, tencent_secret_key


def translate(text, language_from, language_to):
    cred = credential.Credential(tencent_secret_id, tencent_secret_key)
    client = tmt_client.TmtClient(cred, 'ap-shanghai')
    request = tmt_client.models.TextTranslateRequest()
    request.Source = language_from
    request.Target = language_to
    request.SourceText = text
    request.ProjectId = 0
    result = client.TextTranslate(request)
    return result.TargetText
