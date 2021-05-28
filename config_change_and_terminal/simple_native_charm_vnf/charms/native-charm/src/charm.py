#!/usr/bin/env python3

import logging
import os

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.model import (
	MaintenanceStatus,
	ActiveStatus,
)
from ops.main import main

from utils import (
	install_apt,
	fake_service_start,
	fake_service_restart,
	git_clone
)

logger = logging.getLogger(__name__)

APT_REQUIREMENTS = [
	"git",
]
MY_SERVICE = "myfakeservice"
GIT_REPO = "https://github.com/DendoD96/NativeCharmsExamples.git"
SRC_PATH = "/home/ubuntu/repo"


class NativeCharmCharm(CharmBase):
	_stored = StoredState()

	def __init__(self, *args):
		super().__init__(*args)
		self._stored.set_default(serviceStarted=False)

		# Listen to charm events
		self.framework.observe(self.on.config_changed, self.on_config_changed)
		self.framework.observe(self.on.install, self.on_install)
		self.framework.observe(self.on.start, self.on_start)

	def on_config_changed(self, _):
		# We are not aware of which parameter has changed, but in this context we are not interested in,
		# we restart the service (if it was started) with the parameters specified in the configuration.
		if self._stored.serviceStarted:
			self.unit.status = MaintenanceStatus(f"Reloading {MY_SERVICE}")
			fake_service_restart(MY_SERVICE, self.config.get("service_params"))
		self.model.unit.status = ActiveStatus()

	def on_install(self, _):
		self.unit.status = MaintenanceStatus("Installing apt packages")
		install_apt(packages=APT_REQUIREMENTS, update=True)
		if not os.path.exists(SRC_PATH):
			os.makedirs(SRC_PATH)
		self.unit.status = MaintenanceStatus("Cloning this repo to test git apt")
		git_clone(GIT_REPO, output_folder=SRC_PATH)
		self.unit.status = ActiveStatus()

	def on_start(self, _):
		self.unit.status = MaintenanceStatus("Starting fake service")
		fake_service_start(MY_SERVICE, self.config.get("service_params"))
		self._stored.serviceStarted = True
		self.unit.status = ActiveStatus()


if __name__ == "__main__":
	main(NativeCharmCharm)
