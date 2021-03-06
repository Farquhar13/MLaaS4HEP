#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=
"""
File       : workflow.py
Author     : Valentin Kuznetsov <vkuznet AT gmail dot com>
Description: MLaaS4HEP workflow, it provides example how to read ROOT files and train over them ML model
"""

# system modules
import os
import sys
import json
import time
import argparse

# MLaaS4HEP modules
from reader import DataReader
from generator import DataGenerator
from models import train_model, load_model

class OptionParser():
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--model", action="store",
            dest="model", default=None, help="Input model file, see ex_keras.py or ex_pytorch.py for examples")
        self.parser.add_argument("--params", action="store",
            dest="params", default="params.json",
            help="Input model parameters (default params.json)")
        self.parser.add_argument("--specs", action="store",
            dest="specs", default=None, help="Input specs file")
        self.parser.add_argument("--files", action="store",
            dest="files", default='',
            help="either input file with files names or comma separate list of files")
        self.parser.add_argument("--labels", action="store",
            dest="labels", default='',
            help="either input file with labels names/ids or comma separate list of labels")
        self.parser.add_argument("--fout", action="store",
            dest="fout", default=None,
            help="output file name to save pre-trained model")

def main():
    "Main function"
    optmgr  = OptionParser()
    opts = optmgr.parser.parse_args()
    params = json.load(open(opts.params))
    specs = json.load(open(opts.specs)) if opts.specs else None
    if not opts.files:
        print('No files is provided')
        sys.exit(1)
    if os.path.isfile(opts.files):
        files = [f.replace('\n', '') for f in open(opts.files).readlines() if not f.startswith('#')]
    else:
        files = opts.files.split(',')
    if not opts.labels:
        print('No labels is provided')
        sys.exit(1)
    if os.path.isfile(opts.labels):
        labels = [f.replace('\n', '') for f in open(opts.labels).readlines() if not f.startswith('#')]
    else:
        labels = opts.labels.split(',')

    if opts.model:
        train_model(opts.model, files, labels, params, specs, opts.fout)
        return

if __name__ == '__main__':
    main()
