import logging
import logging.config
import os
import sys

from gunicorn import util
from gunicorn.config import Setting, validate_string, validate_bool
from gunicorn.errors import ConfigError
import yaml


LOG = logging.getLogger(__name__)


def get_config(overrides: dict) -> dict:
    """
        :param overrides: config values that overrides the config file(s).
        :type overrides: dict
        :return: a ConfigObj object you can use like a dict
        :rtype: ConfigObj

        :Example:

        get_config(vars(p.parse_args()))

    """
    config_file = os.path.join(overrides['config_dir'], 'main/main.yaml')
    try:
        conf = yaml.load(open(config_file, 'r'))
    except IOError as e:
        print(e)
        print('Configuration file "%s" cannot be found. please fix this and retry.' % config_file)
        sys.exit(1)
    LOG.info('Config file used: %s', config_file)

    return conf

def validate_config_dir(val):
    if val is None:
        return val
    else:
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
    default = None
    desc = """\
        Config directory of your API-Hour Daemon. Example: /etc/hello/
        """

class AutoConfig(Setting):
    name = "auto_config"
    section = "API-Hour"
    cli = ['-ac', "--auto_config"]
    validator = validate_bool
    action = "store_true"
    default = False
    desc = """\
        Enable auto-configuration discover based on daemon name
        """
