import os
import time
from marble.utils.logger import get_logger
from marble.configs.config import Config
from marble.environments.werewolf_env import WerewolfEnv
from marble.evaluator.werewolf_evaluator import WerewolfEvaluator

class WerewolfEngine:
    """
    The WerewolfEngine class orchestrates the Werewolf game simulation,
    initializing and managing the Werewolf-specific environment and evaluator.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the WerewolfEngine with the given configuration path.

        Args:
            config_path (str): Path to the configuration file.
        """
        # Initialize logger
        self.logger = get_logger(self.__class__.__name__)
        
        # Load configuration from the provided path
        self.config_path = config_path
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
        
        # Initialize Environment
        self.environment = WerewolfEnv(name="Werewolf Environment", config_path=config_path)
        self.logger.debug("Werewolf environment initialized.")

        # Set up shared memory path in a dedicated game log directory
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        game_log_dir = os.path.join("werewolf_log", f"game_{timestamp}")
        os.makedirs(game_log_dir, exist_ok=True)
        self.shared_memory_path = os.path.join(game_log_dir, "shared_memory.json")
        
        # Initialize Evaluator with shared memory path and configuration path
        self.evaluator = WerewolfEvaluator(shared_memory_path=self.shared_memory_path, config_path=config_path)
        self.logger.debug("Werewolf evaluator initialized.")

        # Log the successful initialization of the WerewolfEngine
        self.logger.info(f"WerewolfEngine initialized with config path '{config_path}' and game log directory '{game_log_dir}'.")

    def start(self) -> None:
        """
        Start the Werewolf simulation with a single environment start call, 
        relying on shared memory for state management.
        """
        self.logger.info("Starting the Werewolf simulation.")
    
        try:
            # 启动环境，开始一次性模拟
            self.logger.info("ENGINE: Environment started.")
            self.environment.start()
            
        except Exception:
            self.logger.exception("ENGINE: An error occurred during the simulation.")
            raise
        finally:
            # 完成评估
            self.evaluator.finalize()
            self.logger.info("ENGINE: Simulation finalized.")
