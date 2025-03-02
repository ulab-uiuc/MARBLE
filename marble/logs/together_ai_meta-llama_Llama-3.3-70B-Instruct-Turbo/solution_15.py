# solution.py
import pandas as pd
import numpy as np
from typing import Dict, List

# Data Ingestion Module
class DataIngestionModule:
    """
    Module to ingest data from various sources such as CSV, Excel, and database connections.
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
            # Ingest data from CSV file
            data = pd.read_csv(self.file_path)
        elif self.source == 'Excel':
            # Ingest data from Excel file
            data = pd.read_excel(self.file_path)
        else:
            # Ingest data from database connection
            # For simplicity, assume we are using a SQLite database
            import sqlite3
            conn = sqlite3.connect(self.file_path)
            data = pd.read_sql_query("SELECT * FROM data", conn)
            conn.close()
        
        # Validate the data format upon ingestion
        self.validate_data_format(data)
        
        return data

    def validate_data_format(self, data: pd.DataFrame) -> None:
        """
        Validate the data format.

        Args:
        - data (pd.DataFrame): The data to be validated.
        """
        # Check for missing values
        if data.isnull().values.any():
            print("Warning: Missing values found in the data.")
        
        # Check for inconsistent data types
        for column in data.columns:
            if not pd.api.types.is_numeric_dtype(data[column]):
                if not pd.api.types.is_string_dtype(data[column]):
                    print(f"Warning: Inconsistent data type found in column '{column}'.")

# Data Validation Module
class DataValidationModule:
    """
    Module to perform comprehensive data validation.
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
            print("Warning: Duplicate rows found in the data.")
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
                    print(f"Warning: Invalid value found in column '{column}'.")
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
            print("Warning: Missing values found in the data.")
            return False
        
        return True

    def check_validity(self) -> bool:
        """
        Check for data validity.

        Returns:
        - bool: True if the data is valid, False otherwise.
        """
        # Check for invalid values
        for column in self.data.columns:
            if self.data[column].dtype == np.float64:
                if (self.data[column] > 100).any():
                    print(f"Warning: Invalid value found in column '{column}'.")
                    return False
        
        return True

# Data Transformation Module
class DataTransformationModule:
    """
    Module to apply transformation rules to the data.
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
        Apply transformation rules to the data.

        Args:
        - transformations (Dict[str, str]): A dictionary of transformation rules.

        Returns:
        - pd.DataFrame: The transformed data.
        """
        for column, transformation in transformations.items():
            if transformation == 'change_data_type':
                # Change the data type of the column
                self.data[column] = self.data[column].astype(np.float64)
            elif transformation == 'rearrange_columns':
                # Rearrange the columns
                self.data = self.data[[column, *self.data.columns.drop(column)]]
            elif transformation == 'remove_duplicates':
                # Remove duplicate rows
                self.data = self.data.drop_duplicates()
            elif transformation == 'merge_cells':
                # Merge cells
                self.data[column] = self.data[column].fillna('Unknown')
        
        return self.data

# Data Export Module
class DataExportModule:
    """
    Module to export the processed data to various formats.
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
        Export the processed data to the specified format.

        Args:
        - format (str): The format to export the data to (e.g., CSV, Excel, database).
        - file_path (str): The path to the export file.
        """
        if format == 'CSV':
            # Export data to CSV file
            self.data.to_csv(file_path, index=False)
        elif format == 'Excel':
            # Export data to Excel file
            self.data.to_excel(file_path, index=False)
        else:
            # Export data to database table
            # For simplicity, assume we are using a SQLite database
            import sqlite3
            conn = sqlite3.connect(file_path)
            self.data.to_sql('data', conn, if_exists='replace', index=False)
            conn.close()

# DataFlowCoordinator
class DataFlowCoordinator:try:ingestion_module = DataIngestionModule(self.source, self.file_path)
        try:
            ingestion_module = DataIngestionModule(self.source, self.file_path)
        except IOError as e:
            print(f"Error ingesting data: {e}")
            return
        data = ingestion_module.ingest_data()validation_module = DataValidationModule(data)
        if not validation_module.validate_data():transformation_module = DataTransformationModule(data)
        transformed_data = transformation_module.apply_transformations(transformations)export_module = DataExportModule(transformed_data)
        export_module.export_data(export_format, export_file_path)
        try:
            export_module = DataExportModule(transformed_data)
        except sqlite3.Error as e:
            print(f"Error exporting data: {e}")
            return

# Example usage
if __name__ == "__main__":
    coordinator = DataFlowCoordinator('CSV', 'data.csv')
    transformations = {
        'column1': 'change_data_type',
        'column2': 'rearrange_columns'
    }
    coordinator.process_data(transformations, 'Excel', 'processed_data.xlsx')