import os
from . import app_dir
default_dir = os.path.join(app_dir, 'default')
os.makedirs(default_dir, exist_ok=True)


class Config:
    default_engine_path = 'DEFAULT_ENGINE'
    default_language_from_path = 'DEFAULT_LANGUAGE_FROM'
    default_language_to_path = 'DEFAULT_LANGUAGE_TO'
    default_loading_dir_path = 'DEFAULT_LOADING_DIR'
    default_saving_dir_path = 'DEFAULT_SAVING_DIR'
    default_threads_path = 'DEFAULT_THREADS'
    tencent_secret_id_path = 'TENCENT_ID'
    tencent_secret_key_path = 'TENCENT_KEY'
    openai_model_name_path = 'OPENAI_MODEL'
    openai_api_endpoint_path = 'OPENAI_URL'
    openai_api_key_path = 'OPENAI_KEY'

    default_engine_default = 'google'
    default_language_from_default = 'en'
    default_language_to_default = 'zh-CN'
    default_loading_dir_default = os.path.expanduser("~")
    default_saving_dir_default = os.path.expanduser("~")
    default_threads_default = 0
    tencent_secret_id_default = None
    tencent_secret_key_default = None
    openai_model_name_default = 'gpt-3.5-turbo'
    openai_api_endpoint_default = 'https://api.openai.com'
    openai_api_key_default = None

    math_code = '/XMATHX' #better for gpt to understand
    log_file = f'{app_dir}/translate_log'
    raw_mularg_command_list = [('textcolor', 2, (1, ))]
    mularg_command_list = [('textcolor', 2, (1, ))]

    def __init__(self):
        self.load()
        if os.path.exists(f'{app_dir}/TEST'):
            self.test_environment = True
            print('This is a test environment!')
        else:
            self.test_environment = False

    @staticmethod
    def read_variable(path, default):
        if os.path.exists(f'{default_dir}/{path}'):
            return open(f'{default_dir}/{path}').read().replace(' ', '').replace('\n', '')
        else:
            return default

    @staticmethod
    def set_variable(path, default):
        var = input().replace(' ', '').replace('\n', '')
        if var != '':
            print(var, file=open(f'{default_dir}/{path}', 'w'))

    @staticmethod
    def set_variable_4ui(path, var):
        print(var, file=open(f'{default_dir}/{path}', 'w'))

    def load(self):
        self.default_engine = self.read_variable(self.default_engine_path, self.default_engine_default)
        self.default_language_from = self.read_variable(self.default_language_from_path, self.default_language_from_default)
        self.default_language_to = self.read_variable(self.default_language_to_path, self.default_language_to_default)
        self.tencent_secret_id = self.read_variable(self.tencent_secret_id_path, self.tencent_secret_id_default)
        self.tencent_secret_key = self.read_variable(self.tencent_secret_key_path, self.tencent_secret_key_default)
        self.default_loading_dir = self.read_variable(self.default_loading_dir_path, self.default_loading_dir_default)
        self.default_saving_dir = self.read_variable(self.default_saving_dir_path, self.default_saving_dir_default)
        self.default_threads = int(self.read_variable(self.default_threads_path, self.default_threads_default))
        self.openai_model_name = self.read_variable(self.openai_model_name_path,self.openai_model_name_default)
        self.openai_api_endpoint = self.read_variable(self.openai_api_endpoint_path,self.openai_api_endpoint_default)
        self.openai_api_key = self.read_variable(self.openai_api_key_path,self.openai_api_key_default)
        if not os.path.exists(self.default_loading_dir):
            self.default_loading_dir = self.default_loading_dir_default
        if not os.path.exists(self.default_saving_dir):
            self.default_saving_dir = self.default_saving_dir_default


config = Config()
