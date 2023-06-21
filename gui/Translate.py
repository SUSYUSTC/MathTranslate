from mathtranslate.config import config
from mathtranslate.utils import split
from mathtranslate import main
import sys


def translate(file_path, output_path):
    # redirect standard output to log file
    f = open(config.log_file, 'w', encoding='utf-8')
    sys.stdout = f
    sys.stderr = f

    args = split(f'{file_path} -o {output_path}')
    main(args=args)

    print('finished')
    print('file saved to', output_path)

    # restore print
    f.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
