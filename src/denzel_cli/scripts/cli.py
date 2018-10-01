from .. import commands
from .. import config

import click

@click.group()
def cli():
    pass

# -------- startproject --------
@cli.command()
@click.argument('name', type=str)
@click.option('--gpu/--no-gpu', default=False, help="Support for NVIDIA GPU", show_default=True)
def startproject(name, gpu):
    """Builds the denzel project skeleton"""
    commands.create_project(project_name=name, use_gpu=gpu)


# -------- launch --------
@cli.command()
@click.option('--api-port', default=config.API_PORT, type=int, help="API endpoints port", show_default=True)
@click.option('--monitor-port', default=config.MONITOR_PORT, type=int, help="Monitor UI port", show_default=True)
def launch(api_port, monitor_port):
    """Builds and starts all services"""
    commands.launch(api_port, monitor_port)


# -------- shutdown --------
@cli.command()
@click.option('--purge/--no-purge', default=False, help="Discard the docker images", show_default=True)
def shutdown(purge):
    """Stops and deletes all services"""
    commands.shutdown(purge)


# -------- start --------
@cli.command()
def start():
    """Start services"""
    commands.start()


# -------- stop --------
@cli.command()
def stop():
    """Stop services"""
    commands.stop()


# -------- restart --------
@cli.command()
def restart():
    """Restart services"""
    commands.restart()


# -------- status --------
@cli.command()
@click.option('--live/--no-live', default=False,
              help='Live status view', show_default=True)
def status(live):
    """Examine status of services and worker"""
    commands.status(live)


# -------- updatereqs --------
@cli.command()
def updatereqs():
    """Update services according to requirements.txt"""
    commands.updatereqs()


# -------- logs --------
@cli.command()
@click.option('--service', default='all', type=click.Choice(config.SERVICES + ['all']),
              help='Target service', show_default=True)
@click.option('--live/--no-live', default=False,
              help='Follow logs output', show_default=True)
def logs(service, live):
    """Show service logs"""
    commands.logs(service, live)


# -------- logworker --------
@cli.command()
@click.option('--live/--no-live', default=False,
              help='Follow logs output', show_default=True)
def logworker(live):
    """Show worker log"""
    commands.logworker(live)


# -------- shell --------
@cli.command()
@click.option('--service', default='denzel', type=click.Choice(config.SERVICES),
              help='Target service', show_default=True)
def shell(service):
    """Connect to service bash shell"""
    commands.shell(service)
