import os

from click.testing import CliRunner
from denzel_cli.scripts import cli
import pytest


# %% Tests
def test_help():
    """ Sanity check"""
    # Create CLI runner
    runner = CliRunner()

    result = runner.invoke(cli.cli, args=['--help'])

    assert result.exit_code == 0
    assert 'Usage:' in result.output


def test_startproject(tmpdir):
    """
    Test functionality of startproject
    :param tmpdir: tmpdir
    :type tmpdir: py._path.local.LocalPath
    """

    runner = CliRunner()

    # Fail without args
    result = runner.invoke(cli.startproject)
    assert result.exit_code != 0
    assert 'Error: ' in result.output

    with tmpdir.as_cwd():
        # -------- CPU version --------
        result = runner.invoke(cli.startproject, args=['test_project'])

        # Verify command executed
        assert result.exit_code == 0
        assert 'Successfully built' in result.output

        # Verify existence of directories
        created_dirs = set(os.listdir(str(tmpdir) + '/test_project'))
        assert {'app', 'logs', 'docker-compose.yml', 'Dockerfile', 'requirements.txt'}.issubset(created_dirs)
        assert 'pipeline.py' in os.listdir(str(tmpdir) + '/test_project/app/logic')
        assert 'Dockerfile.gpu' not in created_dirs

        # -------- GPU version --------
        result = runner.invoke(cli.startproject, args=['--gpu', 'test_project_gpu'])

        # Verify command executed
        assert result.exit_code == 0
        assert 'Successfully built' in result.output

        # Verify existence of directories
        created_dirs = set(os.listdir(str(tmpdir) + '/test_project_gpu'))
        assert {'app', 'logs', 'docker-compose.yml', 'Dockerfile.gpu', 'requirements.txt'}.issubset(created_dirs)
        assert 'pipeline.py' in os.listdir(str(tmpdir) + '/test_project_gpu/app/logic')
        assert 'Dockerfile' not in created_dirs
