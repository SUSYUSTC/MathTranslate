from .config import config
import json
import requests
from urllib import parse
import openai
import sys
import time

class GPTTranslator:
    def __init__(self):
        self.baseURL=parse.urlparse(config.openai_api_endpoint)._replace(path='/v1')  #make sure using ${host}/v1/chat api
        self.model = config.openai_model_name
        self.key = config.openai_api_key
        self.client=openai.OpenAI(api_key=self.key,base_url=self.baseURL.geturl())


    def format_prompt(self, text, language_to, language_from):
        PROMPT_PROTOTYPE = "As an academic expert with specialized knowledge in various fields, please provide a proficient and precise translation translation from {} to {} of the academic text enclosed in 🔤. It is crucial to maintaining the original phrase or sentence and ensure accuracy while utilizing the appropriate language. Please provide only the translated result without any additional explanation and remove 🔤. The text is as follows:  🔤 {} 🔤  "
        #prompt prototype changed from https://github.com/windingwind/zotero-pdf-translate
        return PROMPT_PROTOTYPE.format(language_from,language_to,text)
    
    def get_server_errormsg(self,error):
        try :
            return error.response.json()['error']['message']
        except Exception :
            return error.message

    def call_openai_api(self,prompt):
        messages= [{
		        "role": "user",
		        "content": prompt
	        }]
        try:
            return self.client.chat.completions.create(model=self.model,temperature=0.8,messages=messages)
        except openai.RateLimitError as e:
            print('API rate limit exceeded, retry after 15s')
            time.sleep(15)
            self.call_openai_api(prompt)
        except openai.InternalServerError as e:
            print('Api server failed({}). retry after 30s.'.format(self.get_server_errormsg(e)))
            time.sleep(30)
            self.call_openai_api(prompt)
        except (openai.PermissionDeniedError,openai.AuthenticationError) as e:
            print('OpenAI api Authentication failed ({}). please check your api setting by:\n translate_tex --setgpt'.format(self.get_server_errormsg(e)))
            sys.exit(-1)
        except openai.APIError as e:
            print('Api requests failed with error:{}. please check your server status'.format(e.message))

            
        

    def translate(self, text, language_to, language_from):
        while True:
            result = self.call_openai_api(self.format_prompt(text, language_to, language_from))
            content_translated = result.choices[0].message.content
            if '🔤' not in content_translated:
                return content_translated

       
