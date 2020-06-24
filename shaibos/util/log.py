# -*- coding: utf-8 -*-

import logging
import logging.config
import os


def get_logger():
    logging_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       '../logging.conf')
    logging.config.fileConfig(logging_config_path)
    return logging.getLogger('shaibos')
