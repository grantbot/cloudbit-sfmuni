"""Module for creating a custom, global, unnamed logger."""

import logging
import logging.config


def setup_global_logger(log_conf):
    logging.config.dictConfig(log_conf)
    return logging.getLogger()
