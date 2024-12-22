import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PROJECT_NAME = "proj"