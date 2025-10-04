from src.config.env_config import env_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def test_env_config():
    assert env_config.WP_USERNAME is not None
    assert env_config.WP_APP_PASSWORD is not None
    assert isinstance(env_config.WP_USERNAME, str)
    assert isinstance(env_config.WP_APP_PASSWORD, str)
    assert len(env_config.WP_USERNAME) > 0
    assert len(env_config.WP_APP_PASSWORD) > 0
    logger.info('Environment variables loaded successfully.')
