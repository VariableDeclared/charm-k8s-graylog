#!/usr/bin/env python3

from utils import sha256_string


GRAYLOG_KEY_MAP = {
    'graylog-pass': "GRAYLOG_ROOT_PASSWORD_SHA2"
}

GRAYLOG_DEFAULT_CONFIGURATION_MAP = {
    'graylog-user': "admin",
    'graylog-pass':  # echo -n "admin" | sha256sum
    "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
}
# TODO: Filter values as they come in
GRAYLOG_CONFIG_FILTER_MAP = {
    'graylog-pass': sha256_string
}


class GraylogConfig:

    _config = {}

    def __init__(self, config):
        self._config = {
            key: GRAYLOG_CONFIG_FILTER_MAP.get(key, lambda x: x)(value)
            for key, value in config.items()
        }

    # think about this
    # def __setattr__(self, name, value):
    #     if name not in self._config

    def __getitem__(self, key):
        if key not in self._config:
            return GRAYLOG_DEFAULT_CONFIGURATION_MAP.get(key, None)
        return self._config[key]

    def render_env_map(self):
        # Return
        # [
        # { NAME: VAL, VALUE: VAL }
        # ]

        return {
            GRAYLOG_KEY_MAP.get(key, key): val
            for key, val in self._config.items()
        }
