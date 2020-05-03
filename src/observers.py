#!/usr/bin/env python3

from abc import abstractmethod
import sys
sys.path.append('lib')
from ops.model import (
    ActiveStatus,
    BlockedStatus,
    WaitingStatus,
    MaintenanceStatus,
)
import logging

logger = logging.getLogger()


class BaseObserver:

    def __init__(self, framework, resources, pod, builder):
        self._framework = framework
        self._resources = resources
        self._pod = pod
        self._builder = builder

    @abstractmethod
    def handle(self, event):
        pass


class ConfigChangeObserver(BaseObserver):

    def handle(self, event):
        for resource in self._resources.keys():
            if not self._resources[resource].fetch(self._framework.resources):
                self._framework.unit_status_set(
                    BlockedStatus(
                        f"Missing or invalid image resource: {resource}"
                    )
                )
                logger.info(f"Missing or invalid image resource: {resource}")
                return
            # Do we need this?
            # if not self._framework.unit_is_leader:

            spec = self._builder.build_spec()
            self._framework.unit_status_set(
                MaintenanceStatus("Configuring Container")
            )
            self._framework.pod_spec_set(spec)

            if self._pod.is_ready:
                self._framework.unit_status_set(ActiveStatus("Ready"))
                logger.info("Pod is ready")
                return

            self._framework.unit_status_set(
                MaintenanceStatus("Pod is not ready")
            )
            logger.info("Pod is not ready")

        if not self._framework.model.relation_get("mongodb"):
            self._framework.unit_status_set(
                WaitingStatus("Waiting for mongodb relation")
            )
            logger.info("Waiting for mongodb relation.")


class RelationObserver(BaseObserver):

    def handle(self, event):
        raise NotImplementedError("Relations are not implemented")
        # data = self.build.buid_relation_data(event.client.formatter)
        # self._framework.relation_data_set(event.relation, data)


class StatusObserver(BaseObserver):

    def handle(self, event):
        if self._pod.is_ready:
            logger.info("Pod is ready")
            self._framework.unit_status_set(ActiveStatus())
            return

        self._framework.unit_status_set(
            BlockedStatus("Pod is not ready")
        )
        logger.info("Pod is not ready")
        logger.debug(f"Pod info: {self._pod}")
