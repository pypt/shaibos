# -*- coding: utf-8 -*-

import os

import sys
import subprocess


def open_file_in_system(path):
    # http://stackoverflow.com/a/435669/200603
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', path))
    elif os.name == 'nt':
        # noinspection PyUnresolvedReferences
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', path))
