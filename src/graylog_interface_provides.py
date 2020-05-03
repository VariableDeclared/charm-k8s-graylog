from ops.framework import (
    EventsBase,
    EventSource,
    Object,
    StoredState
)
from ops.charm import RelationEvent


class NewClientEvent(RelationEvent):

    def restore(self, snapshot):
        super().restore(snapshot)
        self.client = GraylogInterfaceClient(self.relation, self.unit)


class GraylogServerEvents(EventsBase):
    new_client = EventSource(NewClientEvent)


class GraylogServer(Object):
    on = GraylogServerEvents()
    state = StoredState()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.relation_name = relation_name
        self.framework.observe(charm.on.start, self.init_state)
        self.framework.observe(charm.on[relation_name].relation_joined,
                               self.on_joined)
        self.framework.observe(charm.on[relation_name].relation_departed,
                               self.on_departed)

    def init_state(self, event):
        self.state.apps = []

    @property
    def _relations(self):
        return self.model.relations[self.relation_name]

    def on_joined(self, event):
        if event.app not in self.state.apps:
            self.state.apps.append(event.app.name)
            self.on.new_client.emit(GraylogInterfaceClient(event.relation,
                                                           self.model.unit))

    def on_departed(self, event):
        self.state.apps = [app.name for app in self._relations]

    def clients(self):
        return [
            GraylogInterfaceClient(
                relation,
                self.model.unit) for relation in self._relations]


class GraylogInterfaceClient:

    def __init__(self, relation, local_unit):
        self._relation = relation
        self._local_unit = local_unit

    @property
    def name(self):
        return self._relation.name

    @property
    def id(self):
        return self._relation.id

    @property
    def formatter(self):
        return GraylogInterfaceDataFormatter()


class GraylogInterfaceDataFormatter:

    def format(self, graylog_endpoint):
        return {'graylog_endpoint': graylog_endpoint}
