import subprocess
import re
import os

import docker
import click
import requests
from . import config


# -------- Helpers --------
def verify_location(func):
    def command(*args, **kwargs):
        if not os.path.exists('.env'):
            raise click.ClickException("You must be inside project's directory to call this command")

        return func(*args, **kwargs)

    return command


def get_project_name():
    with open('.env') as env_file:
        for line in env_file:
            if 'COMPOSE_PROJECT_NAME' in line:
                name = line.split('=', maxsplit=1)[1].strip()

                return name

    raise FileNotFoundError(".env file not found. Are you in the project's directory?")


def is_port_taken(port):
    return len(subprocess.Popen("netstat -lant | awk '{print $4}' | grep 0.0.0.0:" + str(port),
                                shell=True,
                                stdout=subprocess.PIPE).stdout.read()) > 0


@verify_location
def is_gpu():
    return 'Dockerfile.gpu' in os.listdir(os.getcwd())


@verify_location
def read_env():
    env_data = {}
    with open('.env') as env_file:
        for line in env_file:
            if line:
                key, val = line.split('=', maxsplit=1)
                env_data[key] = val

    return env_data


@verify_location
def get_worker_status():
    try:
        response = requests.get('http://localhost:{}/api/workers?refresh=1&status=1'.format(config.MONITOR_PORT))
        if response.status_code != 200:
            return {'all': config.WORKER_STATUS_DOWN}

        return {worker: config.WORKER_STATUS_UP if up else config.WORKER_STATUS_DOWN
                for worker, up in response.json().items()}

    except requests.exceptions.ConnectionError:
        return {'all': config.WORKER_STATUS_DOWN}


@verify_location
def get_containers_names():
    project_name = get_project_name()
    # Get output of docker-compose ps
    result = subprocess.run(['docker-compose', 'ps'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

    # Find containers' names
    containers_names = {}
    container_name_regex = re.compile('^{project_name}_({services})_[0-9]+'.format(
        project_name=project_name,
        services='|'.join(config.SERVICES)))

    for line in result:

        if not line:  # Skip empty lines
            continue

        line = line.split()
        match = re.match(container_name_regex, line[0])

        if match:
            name = line[0][match.start():match.end()]
            descriptor = name.split('_')[-2]
            containers_names[descriptor] = name

    return containers_names


@verify_location
def get_containers_status():
    client = docker.from_env()
    live_containers = list(map(lambda x: x.name, client.containers.list()))
    containers = get_containers_names()

    # Check for down services
    down_services = []
    up_services = []
    for service_name, service in containers.items():
        if service in live_containers:
            up_services.append(service_name)
        else:
            down_services.append(service_name)

    return up_services, down_services


def is_installed(container, packages):
    """
    Checks whether some pip packages are installed on container or not
    :param container: Container
    :type container: docker.models.containers.Container
    :param packages: PIP packages
    :type packages: collections.Iterable
    :return: List of same length as packages, indicating whether package is installed or not
    :rtype: list
    """

    # Strip versions
    packages = [p.split('=')[0] for p in packages]

    return [container.exec_run('pip show {}'.format(p)).exit_code == 0 for p in packages]


def append_to_requirements(packages):
    with open(config.PIP_REQUIREMENTS_FILE, 'a') as requirements_file:
        requirements_file.write('\n'.join(packages) + '\n')
