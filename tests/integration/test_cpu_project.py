import socket
from contextlib import contextmanager, suppress
from py._path.local import LocalPath
import time
import shutil

import requests
import pytest
from click.testing import CliRunner
from denzel_cli.scripts import cli
from denzel_cli import config as cli_config
from .. import config


# -------- Helpers --------
@contextmanager
def occupy_port(port):
    s = None
    with suppress(OSError):  # Might be already taken
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        s.listen()

    yield

    if s is not None:
        s.close()


@pytest.fixture
def datadir(pytestconfig):
    return pytestconfig.rootdir.join('tests/assets/')


# -------- Tests --------
def test_cpu_project(tmpdir, datadir):
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
            # Launch project on occupied ports
            with occupy_port(cli_config.API_PORT):
                result = runner.invoke(cli.launch)

                assert result.exit_code != 0
                assert 'Error:' in result.output

        # Copy source files to test project directory
        shutil.copy(src='{}/info.txt'.format(datadir), dst=project_dir + '/app/assets/')
        shutil.copy(src='{}/requirements.txt'.format(datadir), dst=project_dir + '/requirements.txt')
        shutil.copy(src='{}/iris_svc.pkl'.format(datadir), dst=project_dir + '/app/assets/')
        shutil.copy(src='{}/pipeline.py'.format(datadir), dst=project_dir + '/app/logic/')
        try:

            with project_dir.as_cwd():

                # Launch project successfully
                result = runner.invoke(cli.launch)

                assert result.exit_code == 0

                # Wait till all are up
                start_time = time.time()

                while True:

                    result = runner.invoke(cli.status)
                    assert result.exit_code == 0

                    if str(result.output).count('UP') < 5:
                        time.sleep(2)
                    else:
                        break  # All is up

                    if time.time() - start_time > 180:
                        raise TimeoutError('Too long installation phase')

            # Check info endpoint
            response = requests.get('http://localhost:8000/info')

            assert response.status_code == 200
            assert 'For prediction' in response.text

            # Check prediction endpoint
            data = {
                "callback_uri": "http://waithook.com/john_q",
                "data": {"a123": {"sepal-length": 4.6, "sepal-width": 3.6, "petal-length": 1.0, "petal-width": 0.2},
                         "b456": {"sepal-length": 6.5, "sepal-width": 3.2, "petal-length": 5.1, "petal-width": 2.0}}
            }
            response = requests.post('http://localhost:8000/predict', json=data)

            assert response.status_code == 200
            response_data = response.json()
            assert response_data['status'].lower() == 'success'

            task_id = response_data['data']['task_id']

            # Check status endpoint
            response = requests.get('http://localhost:8000/status/{}'.format(task_id))

            # Wait for prediction
            start_time = time.time()
            while response.json()['status'].lower() == 'pending' and time.time() - start_time < 10:
                response = requests.get('http://localhost:8000/status/{}'.format(task_id))
                time.sleep(1)

            response_data = response.json()

            assert response.status_code == 200
            assert response_data['status'].lower() == 'success'
            assert response_data['result']['a123'] == 'Iris-setosa'
            assert response_data['result']['b456'] == 'Iris-virginica'

        finally:
            with project_dir.as_cwd():
                # Launch project successfully
                result = runner.invoke(cli.shutdown)
                assert result.exit_code == 0
