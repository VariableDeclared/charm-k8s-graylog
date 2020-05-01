#!/usr/bin/env python3

from config import GraylogConfig


class GraylogBuilder:

    def __init__(self, app_name, config, images, units):
        self._app_name = app_name
        self._config = GraylogConfig(config)
        self._images = images
        self._units = units

    def build_spec(self):
        return self.__make_pod_spec__()

    def __make_container_spec__(self):
        return {
            'containers': [{
                'name': self._app_name,
                'imageDetails': {
                    'imagePath': self._images['graylog-image'].image_path,
                    'username': self._images['graylog-image'].username,
                    'password': self._images['graylog-image'].password
                },
                'config': self._config.render_env_map(),
                'ports': [{
                    'containerPort': 9000,
                    'protocol': 'TCP'
                }]
                # TODO: Liveness probe
                # TODO: readiness probe
            }]
        }

    def __make_pod_spec__(self):
        # TODO: Decide code path
        return self.__make_container_spec__()
