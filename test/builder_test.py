import sys
import unittest
from unittest.mock import (
    patch,
    # MagicMock,
)
sys.path.append('lib')
sys.path.append('src')

# from uuid import uuid4
from builders import GraylogBuilder
from uuid import uuid4
from utils import sha256_string


class GraylogBuilderTest(unittest.TestCase):

    def create_image_resource_obj(self, mock_image_resource, fetch):
        mock_image_resource_obj = mock_image_resource.return_value
        mock_image_resource_obj.fetch.return_value = fetch
        mock_image_resource_obj.image_path = f'{uuid4()}/{uuid4()}'
        mock_image_resource_obj.username = f'{uuid4()}'
        mock_image_resource_obj.password = f'{uuid4()}'
        return mock_image_resource_obj

    @patch('charm.OCIImageResource', autospec=True, spec_set=True)
    def test_spec(self, mock_image_resource_clazz):
        # Setup

        mock_image_resource_obj =\
            self.create_image_resource_obj(mock_image_resource_clazz, True)
        app_name = "test-app"
        config = {
            'graylog-pass': "admin",
            # All keys should be allowed allow for debugging.
            'invalid-key': "keyvalue"
        }
        goal_state_units = None
        images = {
            'graylog-image': mock_image_resource_obj
        }

        builder = GraylogBuilder(
            app_name,
            config,
            images,
            goal_state_units
        )

        spec = builder.build_spec()

        assert spec == {
            'containers': [{
                'name': app_name,
                'imageDetails': {
                    'imagePath': mock_image_resource_obj.image_path,
                    'username': mock_image_resource_obj.username,
                    'password': mock_image_resource_obj.password,
                },
                'config': {
                    'GRAYLOG_ROOT_PASSWORD_SHA2': sha256_string("admin"),
                    'invalid-key': "keyvalue"
                },
                'ports': [{
                    'containerPort': 9000,
                    'protocol': 'TCP'
                }]
                # TODO: Liveness probe
                # TODO: readiness probe
            }]
        }
