import os
import subprocess
from contextlib import suppress
from shutil import copytree, ignore_patterns
from time import sleep

import click
import denzel

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
        env_file.write('image_tag={}\n'.format(config.DENZEL_IMAGE_TAG))
        env_file.write('dockerfile={}\n'.format('Dockerfile' + ('.gpu' if use_gpu else '')))
        env_file.write('runtime={}\n'.format('nvidia' if use_gpu else 'runc'))
        env_file.write('redis_image_tag={}\n'.format(config.REDIS_IMAGE_TAG))

    click.echo('Successfully built ', nl=False)
    click.secho(project_name, fg=config.Colors.DESCRIPTOR.value, nl=False)
    click.echo(' project skeleton')


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

    # Let the user know if using existing image, or creating a new one
    env_data = utils.read_env()
    if utils.image_exists(image_name=env_data['image_name'], image_tag=env_data['image_tag']):
        click.echo('Launching from ', nl=False)
        click.secho('EXISTING', nl=False, fg=config.Colors.SUCCESS.value)
        click.echo(' image')
    else:
        click.echo('Building ', nl=False)
        click.secho('NEW', nl=False, fg=config.Colors.NEUTRAL.value)
        click.echo(' image')

    # Create temporary file for the building stage to be deleted by the startup scripts
    with utils.set_status(config.Status.BUILDING, remove=False):
        command = ['docker-compose', 'up', '-d', '--no-recreate']
        subprocess.run(command)


@utils.verify_location
def shutdown(purge):
    utils.redis_backup(background=False)
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
    utils.redis_backup(background=False)
    command = ['docker-compose', 'stop']
    subprocess.run(command)


@utils.verify_location
def restart():
    stop()
    start()


@utils.verify_location
def status(live):
    # Get status
    service_status = utils.get_containers_status()

    # Get env
    docker_env = utils.read_env()

    # Haven't built yet
    if not service_status[config.Status.DOWN] and not service_status[config.Status.UP]:
        click.echo('Haven\'t been created yet. Did you forget to run "denzel launch"?')
        return

    with suppress(KeyboardInterrupt):
        while True:
            # Clear screen for live sessions
            if live:
                click.clear()

            # Display service statuses
            click.echo('Services:')
            for status, services in service_status.items():
                if services:
                    for service in services:
                        click.echo('\t{} - '.format(service), nl=False)  # Service name
                        click.secho(status.value, fg=utils.status_to_color(status),  # Service status
                                    nl=service not in config.SERVICES_WITH_EXPOSED_PORT or status != config.Status.UP)
                        if service in config.SERVICES_WITH_EXPOSED_PORT and status == config.Status.UP:
                            click.echo(' [ Port: {} ]'.format(docker_env['{}_port'.format(service)]))  # Service port

            # Display worker status
            if 'monitor' in service_status[config.Status.UP]:
                worker_status = utils.get_worker_status()

                for worker, status in worker_status.items():
                    click.echo('Worker: {} - '.format(worker), nl=False)  # Worker name
                    click.secho(status.value, fg=utils.status_to_color(status))  # Worker status

            if not live:
                break

            sleep(1)
            service_status = utils.get_containers_status()


@utils.verify_location
def updateosreqs():
    with utils.set_status(config.Status.UPDATE_OS_REQS):
        # Restart
        restart()


@utils.verify_location
def updatepipreqs():
    with utils.set_status(config.Status.UPDATE_PIP_REQS):
        # Restart
        restart()


@utils.verify_location
def updatereqs():
    with utils.set_status(config.Status.UPDATE_PIP_REQS), utils.set_status(config.Status.UPDATE_OS_REQS):
        # Restart
        restart()


@utils.verify_location
def logs(service, live):
    command = ['docker-compose', 'logs']

    if live:
        command.append('-f')

    if service != 'all':
        command.append(service)

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


@utils.verify_location
def response(sync, timeout):
    utils.set_response_manner(synchronous=sync, timeout=timeout)
