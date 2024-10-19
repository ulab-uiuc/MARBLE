
import yaml

from marble.configs.config import Config
from marble.engine.engine import Engine


def load_config(config_path: str) -> Config:
    """Load YAML configuration and return as a Config object."""
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    return Config(**config_dict)

def main()->None:
    # Load configuration
    config = load_config('config.yaml')

    # Initialize and start the Engine
    engine = Engine(config)
    engine.start()

if __name__ == "__main__":
    main()
