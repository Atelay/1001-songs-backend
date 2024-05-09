import logging
import logging.handlers
import sys

logger = logging.getLogger()


formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

LOG_FILE = "logs/fastapi-app.log"
file = logging.handlers.TimedRotatingFileHandler(
    filename=LOG_FILE, when="midnight", backupCount=5
)
file.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.addHandler(file)
