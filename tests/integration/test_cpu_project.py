import os
import socket
from contextlib import contextmanager
from py._path.local import LocalPath

from click.testing import CliRunner
import docker
import denzel
from denzel_cli.utils import is_port_taken
from denzel_cli.scripts import cli
from denzel_cli import config as cli_config
from .. import config


# -------- Helpers --------
@contextmanager
def occupy_port(port):

    if is_port_taken(port):
        raise ConnectionRefusedError('Port is {} is already occupied'.format(port))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen()

    yield

    s.close()


# -------- Tests --------
def test_cpu_project(tmpdir):
    """
    Test end to end functionality of creating, deploying and using a denzel project (CPU)
    :param tmpdir: tmpdir
    :type tmpdir: py._path.local.LocalPath
    """

    runner = CliRunner()

    with tmpdir.as_cwd():
        # -------- CPU version --------
        result = runner.invoke(cli.startproject, args=['test_project'])

        # Verify command executed
        assert result.exit_code == 0
        assert 'Successfully built' in result.output

        # Verify failing commands outside project dir
        assert all(runner.invoke(cmd).exit_code != 0 for cmd in config.PROJECT_COMMANDS)

        project_dir = LocalPath(str(tmpdir) + '/test_project')

        with project_dir.as_cwd():

            # Append libraries to app requirements.txt
            with open('requirements.txt', 'a') as req_file:
                req_file.write('{}\n'.format('\n'.join(['scikit-learn', 'numpy', 'scipy'])))

            # Launch project on occupied ports
            with occupy_port(cli_config.MONITOR_PORT):
                result = runner.invoke(cli.launch)

                assert result.exit_code != 0
                assert 'Error:' in result.output

            # Launch project successfully
            result = runner.invoke(cli.launch)

            assert result.exit_code == 0

