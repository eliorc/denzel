from enum import Enum

SERVICES = ['api', 'denzel', 'monitor', 'redis']
SERVICES_WITH_EXPOSED_PORT = ['api', 'monitor']

DENZEL_IMAGE_NAME = 'denzel'
DENZEL_IMAGE_TAG = '1.1.0'

DENZEL_IMAGE_SERVICES = ['api', 'denzel', 'monitor']

REDIS_IMAGE_TAG = '4'

WORKER_LOG_PATH = 'logs/worker.log'

PIP_REQUIREMENTS_FILE = 'requirements.txt'

# PORTS
API_PORT = 8000
MONITOR_PORT = 5555


class Status(Enum):
    BUILDING = 'building'
    UPDATE_PIP_REQS = 'updatepipreqs'
    UPDATE_OS_REQS = 'updateosreqs'

    UP = 'UP'
    PIP = 'PIP INSTALLING...'
    OS = 'OS COMMANDS...'
    NA = 'UNAVAILABLE'
    ERROR = 'ERROR'
    LOADING = 'LOADING...'
    DOWN = 'DOWN'


# Colors
class Colors(Enum):
    SUCCESS = 'green'
    FAILURE = 'red'
    DESCRIPTOR = 'blue'
    NEUTRAL = 'yellow'
