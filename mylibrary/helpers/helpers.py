import configparser
import logging
import logging.handlers
import os
import traceback

from mylibrary.helpers import logger


def init_logger(config: configparser.ConfigParser = None) -> logging.Logger:
    """
    initialize a root logger instance
    Returns
    --------
    root_logger: Logger
    """
    logging.getLogger().handlers.clear()
    root_logger = logging.getLogger()
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    try:
        log_format = config["LOGGING"]["FORMAT"]
        log_level = config["LOGGING"]["LEVEL"]
    except (KeyError, TypeError):
        print("Cannot find log format in config, falling back to default log format")
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        log_level = logging.DEBUG
    logging.basicConfig(format=log_format, level=log_level)
    return root_logger


def load_config(config_file):
    """
    This function is used to create and load config file for the api to start:
        * Loads reference config
        * Creates a config file using provided template
        * Loads the newly created config file and returns it
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError("Configuration file not found", f"Could not find configuration file {config_file}")
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_parameter(section, parameter, config):
    """
    get a specific parameter in a config file section
    Parameters:
        section: config file section
        parameter: parameter name in the config file
        config: configParser instance
    """
    try:
        return config[section][parameter]
    except (IndexError, KeyError, TypeError):
        logger.error("Parameter '%s' or section '%s' is/are not defined ", parameter, section)
        return None
    except Exception:
        logger.error("An unknown exception has occurred: %s", traceback.format_exc())
        return None


def is_int(value):
    """
    Check if a given string is convertible to an int or not
    """
    try:
        int(value)
        return True
    except ValueError:
        return False
