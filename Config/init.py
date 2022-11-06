import os
from Config.config import Config, ProductionConfig, DevConfig

def load_config(mode=os.environ.get('ENV')):
    """Load config."""
    try:
        if mode == 'prod':
            return ProductionConfig
        else:
            return DevConfig
    except ImportError:
        return Config