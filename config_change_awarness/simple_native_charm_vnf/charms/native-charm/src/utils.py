import subprocess


def __write_from_terminal(action: str, service_name: str, service_params: str):
	# subprocess.run(["systemctl", action, service_name]).check_returncode()
	text = f"{action} {service_name} with paramteres: {service_params}"
	filepath = f"/home/ubuntu/{service_name}.txt"
	subprocess.run(f"echo {text} >> {filepath}", shell=True)


def fake_service_start(service_name: str, service_params: str):
	__write_from_terminal("start", service_name, service_params)


def fake_service_restart(service_name: str, service_params: str):
	__write_from_terminal("restart", service_name, service_params)
