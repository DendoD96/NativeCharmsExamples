from typing import List, NoReturn

import apt
import subprocess


# Original source code of following functions:
# https://github.com/charmed-osm/srs-enb-ue-operator/blob/master/src/utils.py

def install_apt(packages: List, update: bool = False):
	cache = apt.cache.Cache()
	if update:
		cache.update()
	cache.open()
	for package in packages:
		pkg = cache[package]
		if not pkg.is_installed:
			pkg.mark_install()
	cache.commit()


def git_clone(
		repo: str,
		output_folder: str = None,
		branch: str = None,
		depth: int = None,
):
	command = ["git", "clone"]
	if branch:
		command.append(f"--branch={branch}")
	if depth:
		command.append(f"--depth={depth}")
	command.append(repo)
	if output_folder:
		command.append(output_folder)
	subprocess.run(command).check_returncode()


def __write_from_terminal(action: str, service_name: str, service_params: str):
	# subprocess.run(["systemctl", action, service_name]).check_returncode()
	text = f"{action} {service_name} with paramteres: {service_params}"
	filepath = f"/home/ubuntu/{service_name}.txt"
	subprocess.run(f"echo {text} >> {filepath}", shell=True)


def fake_service_start(service_name: str, service_params: str):
	__write_from_terminal("start", service_name, service_params)


def fake_service_restart(service_name: str, service_params: str):
	__write_from_terminal("restart", service_name, service_params)
