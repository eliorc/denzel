from typing import Optional
import subprocess
import re
import os
from contextlib import contextmanager
from collections import defaultdict

import docker
from docker.errors import ImageNotFound
import click
import requests
from . import config


# -------- Helpers --------
def verify_location(func):
    """ Verifies the current location is in project main directory """

    def command(*args, **kwargs):
        if not os.path.exists('.env'):
            raise click.ClickException("You must be inside project's directory to call this command")

        return func(*args, **kwargs)

    return command


def image_exists(image_name, image_tag):
    """ Checks whether a docker image already exists """

    client = docker.from_env()
    try:
        client.images.get('{image_name}:{image_tag}'.format(image_name=image_name, image_tag=image_tag))
        return True
    except ImageNotFound:
        return False


@verify_location
def get_project_name():
    """ Retrieves project name from the .env file """
    with open('.env') as env_file:
        for line in env_file:
            if 'COMPOSE_PROJECT_NAME' in line:
                name = line.split('=', maxsplit=1)[1].strip()

                return name


def is_port_taken(port):
    """ Checks whether a port is taken or not """

    return len(subprocess.Popen("netstat -lant | awk '{print $4}' | grep 0.0.0.0:" + str(port),
                                shell=True,
                                stdout=subprocess.PIPE).stdout.read()) > 0


def file_to_status(filename):
    """ Given a status filename, gets its Status enum """
    status_string = filename.split('_')[-1].strip('.')

    for status in config.Status:
        if status_string == status.value.split(' ')[0].strip('.').lower():
            return status

    return None


def status_to_color(status):
    """ Given a status enum, gets its ANSI related color """

    if not isinstance(status, config.Status):
        raise ValueError('status must be an enum from config.Status')

    if status == config.Status.UP:
        return config.Colors.SUCCESS.value

    if status == config.Status.DOWN:
        return config.Colors.FAILURE.value

    return config.Colors.NEUTRAL.value


@contextmanager
def set_status(status, service='', remove=True):
    """ Sets a status using a hidden file """

    if not isinstance(status, config.Status):
        raise ValueError('status must be an enum from config.Status')

    status_str = status.value.split(' ')[0].lower().strip('.')

    status_file = '.{}'.format(
        '_'.join([service, status_str]).strip('_'))

    with open(status_file, 'a'):
        pass

    try:
        yield status_file
    finally:
        if remove and os.path.exists(status_file):
            os.remove(status_file)


def redis_backup(background: bool):
    """ Invokes the backing up of Redis (manually creates a data dump) """

    containers_status = get_containers_status()
    if 'redis' not in containers_status[config.Status.UP]:
        return

    # Fetch the redis container
    client = docker.from_env()
    containers_names = get_containers_names()
    redis_container = client.containers.get(containers_names['redis'])

    command = ['redis-cli']
    if background:
        command.append('bgsave')
    else:
        command.append('save')

    redis_container.exec_run(command)


def set_response_manner(synchronous: bool, timeout: float):
    """ Set the state of synchronous responses True == async, False == sync """

    containers_status = get_containers_status()
    if 'redis' not in containers_status[config.Status.UP]:
        return

    # Fetch the redis container
    client = docker.from_env()
    containers_names = get_containers_names()
    redis_container = client.containers.get(containers_names['redis'])

    # Set or del
    command = ['redis-cli', 'set', 'synchronous_timeout']

    if not synchronous:
        timeout = 0.0

    command.append(str(timeout))

    result = redis_container.exec_run(command)

    if result.exit_code != 0:
        raise click.ClickException('Failed to change response manner')

    # Save
    redis_backup(background=True)


@verify_location
def is_gpu():
    """ Checks whether this is a GPU deployment or not """
    return 'Dockerfile.gpu' in os.listdir(os.getcwd())


@verify_location
def read_env():
    """ Retrieves env file as dictionary """
    env_data = {}
    with open('.env') as env_file:
        for line in env_file:
            if line:
                key, val = line.split('=', maxsplit=1)
                env_data[key] = val.strip()

    return env_data


@verify_location
def get_worker_status():
    """ Retrieves worker's status """
    if os.path.exists('.worker_loading'):
        return {'all': config.Status.LOADING}

    try:

        response = requests.get(
            'http://localhost:{}/api/workers?refresh=1&status=1'.format((read_env()['monitor_port'])))
        if response.status_code != 200:
            return {'all': config.Status.ERROR}

        return {worker: config.Status.UP if up else config.Status.DOWN
                for worker, up in response.json().items()}

    except requests.exceptions.ConnectionError:
        return {'api': config.Status.NA}


@verify_location
def get_containers_names():
    """ Retrieves a dictionary mapping service name to its container's name """
    project_name = get_project_name()

    # Get output of docker-compose ps
    client = docker.from_env()
    containers = list(map(lambda x: x.name, client.containers.list(all=True)))

    # Find containers' names
    containers_names = {}
    container_name_regex = re.compile('^{project_name}_({services})_[0-9]+'.format(
        project_name=project_name,
        services='|'.join(config.SERVICES)))

    for container in containers:

        match = re.match(container_name_regex, container)

        if match:
            name = container[match.start():match.end()]
            descriptor = name.split('_')[-2]
            containers_names[descriptor] = name

    return containers_names


@verify_location
def get_containers_status():
    """ Retrieves a dictionary mapping status to its service name"""
    # Init status dictionary
    status = defaultdict(list)

    client = docker.from_env()
    live_containers = list(map(lambda x: x.name, client.containers.list()))
    containers = get_containers_names()

    # Get status files
    status_files = [f for f in os.listdir('.') if f.startswith('.')]
    for service_name, service in containers.items():

        if service in live_containers:
            service_status_file = [f for f in status_files if re.match(r'\.{}'.format(service_name), f)]
            if service_status_file:  # Status by file
                status[file_to_status(service_status_file[0])].append(service_name)
            else:
                status[config.Status.UP].append(service_name)
        else:
            status[config.Status.DOWN].append(service_name)

    return status
