import os
import subprocess
from itertools import compress
from shutil import copytree, ignore_patterns

import click
import denzel
import docker

from . import utils
from . import config


# -------- Command line calls --------
def create_project(project_name, use_gpu):
    # Validate project directory was not already created
    destination = './{}'.format(project_name)
    if os.path.exists(destination):
        raise click.ClickException('The directory "{}" already exists'.format(project_name))

    # Use GPU?
    dockerfile_to_ignore = 'Dockerfile' if use_gpu else 'Dockerfile.gpu'

    ignore = ignore_patterns(dockerfile_to_ignore, '__pycache__')

    # Create project main directory
    source = denzel.__path__[0]
    copytree(source, destination, ignore=ignore)

    # Create .env file
    with open('{}/.env'.format(destination),
              'w') as env_file:
        env_file.write('COMPOSE_PROJECT_NAME={}\n'.format(project_name))
        env_file.write('api_port={}\n'.format(config.API_PORT))
        env_file.write('monitor_port={}\n'.format(config.MONITOR_PORT))
        env_file.write('image_name={}\n'.format(config.DENZEL_IMAGE_NAME + ('-gpu' if use_gpu else '')))
        env_file.write('dockerfile={}\n'.format('Dockerfile' + ('.gpu' if use_gpu else '')))
        env_file.write('runtime={}\n'.format('nvidia' if use_gpu else 'runc'))
        env_file.write('redis_image_tag={}\n'.format(config.REDIS_IMAGE_TAG))

    click.echo('Successfully built {} project skeleton'.format(project_name))


@utils.verify_location
def launch(api_port, monitor_port):
    # Checks if project already launched
    if utils.get_containers_names():
        raise click.ClickException('Project already launched! Did you mean to run "denzel start"?')

    if utils.is_port_taken(api_port):
        raise click.ClickException('Port {} is already taken! Pass an available port using the --api-port option')

    if utils.is_port_taken(monitor_port):
        raise click.ClickException('Port {} is already taken! Pass an available port using the --monitor-port option')

    # Change .env file
    with open('.env') as env_file:  # Read
        env_data = env_file.readlines()

    with open('.env', 'w') as env_file:  # Write
        for data_line in env_data:
            if 'api_port' in data_line:
                env_file.write('api_port={}\n'.format(api_port))  # API port
            elif 'monitor_port' in data_line:
                env_file.write('monitor_port={}\n'.format(monitor_port))  # Monitor port
            else:
                env_file.write(data_line)

    command = ['docker-compose', 'up', '-d', '--no-recreate']
    subprocess.run(command)


@utils.verify_location
def shutdown(purge):
    command = ['docker-compose', 'down']

    if purge:
        command += ['--rmi', 'all']
    subprocess.run(command)


@utils.verify_location
def start():
    command = ['docker-compose', 'start']
    subprocess.run(command)


@utils.verify_location
def stop():
    command = ['docker-compose', 'stop']
    subprocess.run(command)


@utils.verify_location
def restart():
    stop()
    start()


@utils.verify_location
def status():
    up_services, down_services = utils.get_containers_status()

    # Haven't built yet
    if not down_services and not up_services:
        click.echo('Services: Haven\'t been created yet. Did you forget to run "denzel launch"?')
        return

    # All down
    if not up_services:
        click.echo('Services: All down. Did you forget to run "denzel start"?')
        return

    # All up
    if not down_services:
        click.echo('Services: All up!')

    # Some down, some up
    else:
        click.echo(
            'Services: {down_services} are down. Check respective logs to see what went wrong ("denzel logs")'.format(
                down_services=', '.join(down_services)))

    # Worker status
    if 'monitor' in up_services:
        worker_status = utils.get_worker_status()
        click.echo('Workers:')
        for worker, status in worker_status.items():
            click.echo('\t{} - {}'.format(worker, status))


@utils.verify_location
def pinstall(service, upgrade, req_append, packages):
    if not packages:
        raise click.ClickException('No packages supplied')

    # Remove duplicates
    packages = list(set(packages))

    # Get docker client
    client = docker.from_env()

    # Resolve service name to container
    container_name = utils.get_containers_names()[service]

    # Get running containers
    containers = {c.name: c for c in client.containers.list()}

    # Check target container is running
    if container_name not in containers:
        raise click.ClickException('Target container is down! Did you forget to run "denzel start"?')

    # Check if the packages are already installed
    installation_status = utils.is_installed(container=containers[container_name],
                                             packages=packages)
    if not upgrade:
        for installed in compress(packages, installation_status):
            click.echo(
                '{} is already installed, skipping. If you wish to upgrade, use the --upgrade flag.'.format(installed))

        if all(installation_status):  # If all packages already installed
            return

    new_packages = list(compress(packages, map(lambda x: not x, installation_status)))

    # Run pip install
    command = ['docker', 'exec', container_name, 'pip', 'install']
    if upgrade:
        command.append('--upgrade')

    command += packages if upgrade else new_packages

    # Install
    subprocess.run(command)

    # Append to requirements file
    if req_append:
        # Verify installation
        installation_status = utils.is_installed(container=containers[container_name],
                                                 packages=new_packages)
        successfully_installed = list(compress(new_packages, installation_status))

        if successfully_installed:
            utils.append_to_requirements(packages=successfully_installed)


@utils.verify_location
def updatereqs(service, upgrade, restart_services=True):
    # Get docker client
    client = docker.from_env()

    # Resolve service name to container
    container_name = utils.get_containers_names()[service]

    # Get running containers
    containers = {c.name: c for c in client.containers.list()}

    # Check target container is running
    if container_name not in containers:
        raise click.ClickException('Target container is down! Did you forget to run "denzel start"?')

    # Run pip install
    command = ['docker', 'exec', container_name, 'pip', 'install', '-r']
    if upgrade:
        command.append('--upgrade')

    # Install
    subprocess.run(command)

    # Restart
    if restart_services:
        restart()


@utils.verify_location
def logs(service, live):
    command = ['docker-compose', 'logs']
    if service != 'all':
        command.append(service)

    if live:
        command.append('-f')

    subprocess.run(command)


@utils.verify_location
def logworker(live):
    if not os.path.exists(config.WORKER_LOG_PATH):
        raise click.ClickException('Worker log hasn\'t been created yet')

    if live:
        command = ['tail', '-f', config.WORKER_LOG_PATH]
    else:
        command = ['cat', config.WORKER_LOG_PATH]

    subprocess.run(command)


@utils.verify_location
def shell(service):
    container_names = utils.get_containers_names()
    command = ['docker', 'exec', '-it', container_names[service], 'bash']
    subprocess.run(command)
