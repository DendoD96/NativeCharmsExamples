#!/usr/bin/env python3

import logging

from ops.charm import CharmBase
from ops.model import (
    MaintenanceStatus,
    ActiveStatus,
)
from ops.framework import StoredState
from ops.main import main

from utils import (
    fake_service_start,
    fake_service_restart,
)

logger = logging.getLogger(__name__)

MY_SERVICE = "myfakeservice"


class NativeCharmCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self._stored.set_default(serviceStarted=False)
        self._stored.set_default(previous_config=None)

        # Listen to charm events
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)

    def on_config_changed(self, _):
        previous_config = self._stored.previous_config
        if previous_config is not None:
            # get the new values if they have changed
            differences = dict(set(self.model.config.items()) - previous_config)
            if 'service_params' in differences and self._stored.serviceStarted:
                self.unit.status = MaintenanceStatus(f"Reloading {MY_SERVICE}")
                fake_service_restart(MY_SERVICE, self.config.get("service_params"))
        self._stored.previous_config = set(self.model.config.items())
        self.model.unit.status = ActiveStatus()

    def on_install(self, _):
        self.unit.status = ActiveStatus()

    def on_start(self, _):
        self.unit.status = MaintenanceStatus("Starting fake service")
        fake_service_start(MY_SERVICE, self.config.get("service_params"))
        self._stored.serviceStarted = True
        self.unit.status = ActiveStatus()


if __name__ == "__main__":
    main(NativeCharmCharm)
