from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client
from .config import tencent_secret_id, tencent_secret_key, math_code


class Translator:
    def __init__(self):
        self.cred = credential.Credential(tencent_secret_id, tencent_secret_key)
        self.client = tmt_client.TmtClient(self.cred, 'ap-shanghai')

    def translate(self, text, language_to, language_from):
        request = tmt_client.models.TextTranslateRequest()
        request.Source = language_from
        request.Target = language_to
        request.SourceText = text
        request.ProjectId = 0
        request.UntranslatedText = math_code
        result = self.client.TextTranslate(request)
        return result.TargetText
