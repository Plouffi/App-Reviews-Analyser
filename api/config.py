import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = yaml.safe_load(open(f"{ROOT_DIR}/resources/config.yaml"))