import os
from dotenv import load_dotenv
from Config.config import Config, ProductionConfig, DevConfig

load_dotenv()


def load_config(mode=os.getenv('ENV', 'prod')):
    """Load config."""
    if mode == 'prod':
        return ProductionConfig
    else:
        return DevConfig

