#!/usr/bin/env python
import os
import sys
from . import utils
from .translate import translate_single_tex_file


def main(args=None, require_updated=True):
    '''
    to call this function from python,
    you can do e.g `main(['input.tex', '-o', 'output.tex'])`
    '''
    utils.check_update(require_updated=require_updated)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', type=str, help='input file')
    parser.add_argument("-o", type=str, help='output path')
    utils.add_arguments(parser)
    parser.add_argument("--compile", action='store_true')
    parser.add_argument("--overwrite", action='store_true')
    options = parser.parse_args(args)
    utils.process_options(options)

    if options.file is None:
        parser.print_help()
        sys.exit()

    input_path = options.file
    if options.o is None:
        input_path_base, input_path_ext = os.path.splitext(input_path)
        if input_path_ext == '.tex':
            if not options.overwrite:
                print("The input file ends with .tex, it will be overwritten.")
                print("If you confirm this action, please press enter, otherwise ctrl+C to cancel")
                input()
                print('OK I will continue')
        output_path = input_path_base + '.tex'
    else:
        output_path = options.o

    translate_single_tex_file(input_path, output_path, options.engine, options.l_from, options.l_to, options.debug)
    if options.compile:
        os.system(f'xelatex {output_path}')
    else:
        print(f"You can then compile it locally by running 'xelatex {output_path}' or compile it online on overleaf")
