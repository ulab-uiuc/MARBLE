"""
Data loader module for loading tasks or datasets.
"""

import json
import os
from typing import Any


class DataLoader:
    """
    DataLoader class for loading tasks or datasets from files.
    """
    def __init__(self, data_path: str):
        """
        Initialize the DataLoader with the path to the data file.

        Args:
            data_path (str): Path to the data file.
        """
        self.data_path = data_path

    def load_data(self) -> Any:
        """
        Load data from the data file.

        Returns:
            List[Dict[str, Any]]: List of data items.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at path: {self.data_path}")

        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

# Example usage:
# data_loader = DataLoader('data/tasks.json')
# tasks = data_loader.load_data()
