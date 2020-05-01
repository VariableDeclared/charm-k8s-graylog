#!/usr/bin/env python3


import logging
import sys
sys.path.append('lib')
from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from resources import OCIImageResource
from wrapper import FrameworkWrapper
from builders import GraylogBuilder
from k8s import K8sPod
from observers import (
    ConfigChangeObserver,
    StatusObserver,
)

logger = logging.getLogger()


class CharmGraylog(CharmBase):
    _state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self._framework_wrapper = FrameworkWrapper(self.framework, self._state)
        self._resources = {
            'graylog-image': OCIImageResource('graylog-image')
        }

        self._graylog_builder = GraylogBuilder(
            self._framework_wrapper.app_name,
            self._framework_wrapper.config,
            self._resources,
            self._framework_wrapper.goal_state_units
        )

        # TODO: Sidecar

        self._pod = K8sPod(self._framework_wrapper.app_name)
        # TODO: Relations

        delegators = [
            (self.on.start, self.on_config_changed_delegator),
            (self.on.upgrade_charm, self.on_config_changed_delegator),
            (self.on.config_changed, self.on_config_changed_delegator),
            (self.on.update_status, self.on_update_status_delegator)
        ]

        for delegator in delegators:
            self.framework.observe(delegator[0], delegator[1])

    def on_config_changed_delegator(self, event):

        return ConfigChangeObserver(
            self._framework_wrapper,
            self._resources,
            self._pod,
            self._graylog_builder
        ).handle(event)

    def on_update_status_delegator(self, event):
        logger.info(f"on_updae_status delegator {event}")
        return StatusObserver(
            self._framework_wrapper,
            self._resources,
            self._pod,
            self._graylog_builder
        ).handle(event)


if __name__ == "__main__":
    main(CharmGraylog)
