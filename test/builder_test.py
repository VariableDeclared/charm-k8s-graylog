import sys
import unittest
from unittest.mock import (
    patch,
    MagicMock,
)
sys.path.append('lib')
sys.path.append('src')

from uuid import uuid4
from builders import GraylogBuilder


class GraylogBuilderTest(unittest.TestCase):

    @patch('charm.OCIImageResource', autospec=True, spec_set=True)
    def test_spec(self, mock_image_resource_clazz):
        # Setup

        mock_image_resource_obj =\
            self.create_image_resource_obj(mock_image_resource_clazz, True)
        app_name = "test-app"
        config = {
            'graylog-password': "admin",
            'invalid-key': "keyvalue"
        }
        goal_state_units = None
        images = {
            'mongodb-image': mock_image_resource_obj
        }

        builder = GraylogBuilder(
            app_name,
            config,
            images,
            goal_state_units
        )

        spec = builder.build_spec()

        assert spec == {
            # TODO: Make spec
            'spec': {
                'containers': [{
                    'name': app_name,
                    'imageDetails': {
                        'imagePath': mock_image_resource_obj.image_path,
                        'username': mock_image_resource_obj.username,
                        'password': mock_image_resource_obj.password,
                    },
                    'config': {
                        'GRAYLOG_ROOT_PASSWORD_SHA2':
                        "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
                    },
                    'ports': [{
                        'containerPort': 9000,
                        'protocol': 'TCP'
                    }]
                    # TODO: Liveness probe
                    # TODO: readiness probe
                }
            ]
        }
    }