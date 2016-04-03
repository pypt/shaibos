# -*- coding: utf-8 -*-

import logging
import logging.config
import os


def get_logger():
    logging.config.fileConfig(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../logging.conf'))
    return logging.getLogger('iv')
