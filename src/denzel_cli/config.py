SERVICES = ['api', 'denzel', 'monitor', 'redis']

DENZEL_IMAGE_NAME = 'denzel'

DENZEL_IMAGE_SERVICES = ['api', 'denzel', 'monitor']

REDIS_IMAGE_TAG = '4'

WORKER_LOG_PATH = 'logs/worker.log'

PIP_REQUIREMENTS_FILE = 'requirements.txt'

# PORTS
API_PORT = 8000
MONITOR_PORT = 5555

# Worker status
WORKER_STATUS_UP = 'UP'
WORKER_STATUS_DOWN = 'DOWN'
