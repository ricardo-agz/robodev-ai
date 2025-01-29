import time
from NeutrinoAI.ai_generator import AIBuildfileGenerator
from generator.Config.logger import logger
from generator.Config.init import load_config

config = load_config()


def sleep(seconds):
    logger.info(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    logger.info("Done sleeping")
    return f"Slept for {seconds} seconds"


def get_buildfile_neutrinoai(description):
    logger.info(f"Generating Buildfile for app: {description[:25]}...")
    neutrino_ai = AIBuildfileGenerator(app_description=description, mock=config.MOCK_AI)
    json_buildfile = neutrino_ai.get_buildfile_json()
    
    return json_buildfile