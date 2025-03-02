# solution.py
import pandas as pd
import numpy as np
from typing import Dict, List

# Data Ingestion Module
class DataIngestionModule:
    """
    This module is responsible for ingesting data from various sources such as CSV, Excel, and database connections.
    It validates the data format upon ingestion and handles large datasets.
    """
    def __init__(self, source: str, file_path: str):
        """
        Initialize the DataIngestionModule.

        Args:
        - source (str): The source of the data (e.g., CSV, Excel, database).
        - file_path (str): The path to the data file.
        """
        self.source = source
        self.file_path = file_path

    def ingest_data(self) -> pd.DataFrame:
        """
        Ingest data from the specified source.

        Returns:
        - pd.DataFrame: The ingested data.
        """
        if self.source == 'CSV':
            # Read CSV file
            data = pd.read_csv(self.file_path)
        elif self.source == 'Excel':
            # Read Excel file
            data = pd.read_excel(self.file_path)
        else:
            # Handle other sources (e.g., database connections)
            raise NotImplementedError("Only CSV and Excel sources are currently supported")
        
        # Validate data format
        self.validate_data_format(data)
        
        return data

    def validate_data_format(self, data: pd.DataFrame) -> None:
        """
        Validate the format of the ingested data.

        Args:
        - data (pd.DataFrame): The ingested data.
        """
        # Check for missing values
        if data.isnull().values.any():
            print("Warning: Missing values detected in the data.")
        
        # Check for inconsistent data types
        for column in data.columns:
            if not pd.api.types.is_numeric_dtype(data[column]):
                if not pd.api.types.is_string_dtype(data[column]):
                    print(f"Warning: Column '{column}' has an inconsistent data type.")

# Data Validation Module
class DataValidationModule:
    """
    This module performs comprehensive data validation, including checks for data consistency, accuracy, completeness, and validity.
    It ensures that the data is clean and ready for further processing.
    """
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the DataValidationModule.

        Args:
        - data (pd.DataFrame): The data to be validated.
        """
        self.data = data

    def validate_data(self) -> bool:
        """
        Perform comprehensive data validation.

        Returns:
        - bool: True if the data is valid, False otherwise.
        """
        # Check for data consistency
        if not self.check_consistency():
            return False
        
        # Check for data accuracy
        if not self.check_accuracy():
            return False
        
        # Check for data completeness
        if not self.check_completeness():
            return False
        
        # Check for data validity
        if not self.check_validity():
            return False
        
        return True

    def check_consistency(self) -> bool:
        """
        Check for data consistency.

        Returns:
        - bool: True if the data is consistent, False otherwise.
        """
        # Check for duplicate rows
        if self.data.duplicated().any():
            print("Warning: Duplicate rows detected in the data.")
            return False
        
        return True

    def check_accuracy(self) -> bool:
        """
        Check for data accuracy.

        Returns:
        - bool: True if the data is accurate, False otherwise.
        """
        # Check for invalid values
        for column in self.data.columns:
            if self.data[column].dtype == np.float64:
                if (self.data[column] < 0).any():
                    print(f"Warning: Invalid values detected in column '{column}'.")
                    return False
        
        return True

    def check_completeness(self) -> bool:
        """
        Check for data completeness.

        Returns:
        - bool: True if the data is complete, False otherwise.
        """
        # Check for missing values
        if self.data.isnull().values.any():
            print("Warning: Missing values detected in the data.")
            return False
        
        return True

    def check_validity(self) -> bool:
        """
        Check for data validity.

        Returns:
        - bool: True if the data is valid, False otherwise.
        """
        # Check for invalid data types
        for column in self.data.columns:
            if not pd.api.types.is_numeric_dtype(self.data[column]):
                if not pd.api.types.is_string_dtype(self.data[column]):
                    print(f"Warning: Invalid data type detected in column '{column}'.")
                    return False
        
        return True

# Data Transformation Module
class DataTransformationModule:
    """
    This module allows users to define and apply transformation rules to the data.
    It supports transformations such as changing data types, rearranging columns, removing duplicates, and merging cells.
    """
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the DataTransformationModule.

        Args:
        - data (pd.DataFrame): The data to be transformed.
        """
        self.data = data

    def apply_transformations(self, transformations: Dict[str, str]) -> pd.DataFrame:
        """
        Apply the specified transformations to the data.

        Args:
        - transformations (Dict[str, str]): A dictionary of transformations to apply.

        Returns:
        - pd.DataFrame: The transformed data.
        """
        # Apply transformations
        for column, transformation in transformations.items():
            if transformation == 'change_type':
                # Change data type
                self.data[column] = pd.to_numeric(self.data[column])
            elif transformation == 'rearrange':
                # Rearrange columns
                self.data = self.data[[column] + [c for c in self.data.columns if c != column]]
            elif transformation == 'remove_duplicates':
                # Remove duplicates
                self.data = self.data.drop_duplicates()
            elif transformation == 'merge_cells':
                # Merge cells
                self.data[column] = self.data[column].apply(lambda x: ' '.join(x.split()))
        
        return self.data

# Data Export Module
class DataExportModule:
    """
    This module exports the processed data to various formats, including CSV, Excel, and database tables.
    """
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the DataExportModule.

        Args:
        - data (pd.DataFrame): The data to be exported.
        """
        self.data = data

    def export_data(self, format: str, file_path: str) -> None:
        """
        Export the data to the specified format.

        Args:
        - format (str): The format to export the data to (e.g., CSV, Excel).
        - file_path (str): The path to export the data to.
        """
        if format == 'CSV':
            # Export to CSV
            self.data.to_csv(file_path, index=False)
        elif format == 'Excel':
            # Export to Excel
            self.data.to_excel(file_path, index=False)
        else:
            # Handle other formats (e.g., database tables)
            raise NotImplementedError("Only CSV and Excel formats are currently supported")

# DataFlowCoordinator
class DataFlowCoordinator:def coordinate_data_flow(self) -> None:
    try:    # Ingest data
        ingestion_module = DataIngestionModule(self.source, self.file_path)
        data = ingestion_module.ingest_data()
        
        # Validate data
        validation_module = DataValidationModule(data)
        if not validation_module.validate_data():
            print("Data validation failed. Aborting data flow.")
            return
        
        # Transform data
        transformation_module = DataTransformationModule(data)
        transformations = {
            'column1': 'change_type',
            'column2': 'rearrange',
            'column3': 'remove_duplicates',
            'column4': 'merge_cells'
        }
        data = transformation_module.apply_transformations(transformations)
        
        # Export data
        export_module = DataExportModule(data)
        export_module.export_data('CSV', 'output.csv')
        # Validate transformation result
        if data.empty:
            raise ValueError('Data is empty after transformation')

# Example usage
if __name__ == '__main__':
    coordinator = DataFlowCoordinator('CSV', 'input.csv')
    coordinator.coordinate_data_flow()