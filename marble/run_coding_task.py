from marble.configs.config import Config
from marble.engine.engine import Engine

def main():
    # Load the coding configuration
    config_path = "configs/coding_config.yaml"
    config = Config(config_path)
    
    # Initialize and run the engine
    engine = Engine(config)
    engine.start()

if __name__ == "__main__":
    main()