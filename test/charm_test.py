import sys
sys.path.append('lib')
sys.path.append('src')
import unittest
from ops.testing import Harness
# from ops import (charm, framework, model)
from charm import CharmGraylog
from unittest.mock import (
    patch
)


class CharmTest(unittest.TestCase):

    @patch('wrapper.FrameworkWrapper.goal_state_units', autospec=True)
    def test_set_leader(self, *args):
        harness = Harness(CharmGraylog)
        harness.begin()
        harness.set_leader(False)
        self.assertFalse(harness.charm.model.unit.is_leader())
