import os
from dotenv import load_dotenv
from generator.Config.config import ProductionConfig, DevConfig

load_dotenv()


def load_config(mode=os.getenv('ENV', 'prod')):
    """Load config."""
    if mode == 'prod':
        return ProductionConfig
    else:
        return DevConfig

