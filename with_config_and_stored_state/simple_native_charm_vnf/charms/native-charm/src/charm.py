#!/usr/bin/env python3

import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

from utils import (
    write
)

logger = logging.getLogger(__name__)


class NativeCharmCharm(CharmBase):

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self._stored.set_default(counter=0)

        # Listen to charm events
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)

        self.framework.observe(self.on.incrementcounter_action, self.on_increment_counter)

    def on_config_changed(self, event):
        """Handle changes in configuration"""
        self.model.unit.status = ActiveStatus()

    def on_install(self, event):
        """Called when the charm is being installed"""
        self.model.unit.status = ActiveStatus()

    def on_start(self, event):
        """Called when the charm is being started"""
        self.model.unit.status = ActiveStatus()

    def on_increment_counter(self, event):
        filepath=self.config.get("filepath")
        write(filepath, str(self._stored.counter))
        self._stored.counter += 1
        event.set_results({"edited": True, "filename": filepath})    

if __name__ == "__main__":
    main(NativeCharmCharm)
