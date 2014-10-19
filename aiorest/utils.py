import logging
import logging.config
import os
import signal
import sys
from configparser import NoSectionError

from configobj import ConfigObj


STOP_SIGNALS = (signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGABRT, signal.SIGTERM)


def get_config(overrides: dict) -> ConfigObj:
    """
        :param overrides: config values that overrides the config file(s).
        :type overrides: dict
        :return: a ConfigObj object you can use like a dict
        :rtype: ConfigObj

        :Example:

        get_config(vars(p.parse_args()))

    """
    try:
        config_file = os.path.join(overrides['config_dir'], 'main.conf')
        #Interpolation=False could be important, if we have postgresql queries in configuration
        conf = ConfigObj(config_file, file_error=True)
    except IOError as e:
        print(e)
        print('Configuration file "%s" cannot be found. please fix this and retry.' % config_file)
        sys.exit(1)

    try:
        logging_file = os.path.join(overrides['config_dir'], 'logging.ini')
        logging.config.fileConfig(logging_file, disable_existing_loggers=False)
    except (NoSectionError, KeyError) as e:
        print(e)
        print('Your logging file is wrong or is missing, please provide a correct one: [%s]' % logging_file)
        sys.exit(1)

    return conf
