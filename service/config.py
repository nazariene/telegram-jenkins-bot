import os
import configparser

global config


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


config = configparser.ConfigParser(interpolation=EnvInterpolation())
config.read('config.cfg')
