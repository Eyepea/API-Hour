import logging
import logging.config
import os
import sys
from configparser import NoSectionError

from configobj import ConfigObj
from gunicorn import util
from gunicorn.config import Setting, validate_string
from gunicorn.errors import ConfigError


LOG = logging.getLogger(__name__)


def get_config(overrides: dict) -> ConfigObj:
    """
        :param overrides: config values that overrides the config file(s).
        :type overrides: dict
        :return: a ConfigObj object you can use like a dict
        :rtype: ConfigObj

        :Example:

        get_config(vars(p.parse_args()))

    """
    config_file = os.path.join(overrides['config_dir'], 'main.conf')
    try:
        #interpolation=False could be important, if we have %s in configuration
        conf = ConfigObj(config_file, interpolation=False, file_error=True)
    except IOError as e:
        print(e)
        print('Configuration file "%s" cannot be found. please fix this and retry.' % config_file)
        sys.exit(1)

    logging.captureWarnings(True)
    logging_file = os.path.join(overrides['config_dir'], 'logging.ini')
    try:
        logging.config.fileConfig(logging_file, disable_existing_loggers=False)
    except (NoSectionError, KeyError) as e:
        print(e)
        print('Your logging file is wrong or is missing, please provide a correct one: [%s]' % logging_file)
        sys.exit(1)

    LOG.info('Config file used: %s', config_file)

    return conf

def validate_config_dir(val):
    # valid if the value is a string
    val = validate_string(val)

    # transform relative paths
    path = os.path.abspath(os.path.normpath(os.path.join(util.getcwd(), val)))

    # test if the path exists
    if not os.path.exists(path):
        raise ConfigError("can't find a config directory in %r" % val)

    return path

class ConfigDir(Setting):
    name = "config_dir"
    section = "API-Hour"
    cli = ["--config_dir"]
    validator = validate_config_dir
    default = ''
    desc = """\
        Config directory of your API-Hour Daemon. Example: /etc/hello/
        """
