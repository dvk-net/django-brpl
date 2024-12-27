import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PROJECT_NAME = "proj"

LOCAL_SETTINGS_STATIC_MEDIA_CHANGES_DOCKER_DEV =  {
    # `look for`: `change to` format
    "STATIC_URL": "STATIC_URL = 'static/'",
    "STATIC_ROOT": "STATIC_ROOT = '/var/www/static'",
    "MEDIA_URL": "MEDIA_URL = 'media/'",
    "MEDIA_ROOT": "MEDIA_ROOT = '/var/www/media'",
}
LOCAL_SETTINGS_STATIC_MEDIA_CHANGES_INIT_DEV =  {
    # `look for`: `change to` format
    "STATIC_URL": "STATIC_URL = 'static/'",
    "STATIC_ROOT": "STATIC_ROOT = '../static'",
    "MEDIA_URL": "MEDIA_URL = 'media/'",
    "MEDIA_ROOT": "MEDIA_ROOT = '../media'",
}
