# solution.py

import pandas as pd
import numpy as np

class DataFlowCoordinator:
    def __init__(self):
        self.data = None

    def ingest_data(self, source, file_type):
        """
        Ingest data from various sources (CSV, Excel).
        Validates the data format upon ingestion.
        """
        if file_type == 'csv':
            self.data = pd.read_csv(source)
        elif file_type == 'excel':
            self.data = pd.read_excel(source)
        else:
            raise ValueError("Unsupported file type. Use 'csv' or 'excel'.")

        # Validate data format
        if self.data.empty:
            raise ValueError("Ingested data is empty.")
        print("Data ingestion completed successfully.")

    def validate_data(self):
        """
        Perform comprehensive data validation checks.
        Ensures data consistency, accuracy, completeness, and validity.
        """
        if self.data is None:
            raise ValueError("No data to validate. Please ingest data first.")

        # Example validation checks        # Check for null values
        if self.data.isnull().values.any():
            raise ValueError("Data contains null values.")

        # Check for duplicates
        if self.data.duplicated().any():
            raise ValueError("Data contains duplicate entries.")def validate_data(self, required_fields, expected_types):
        """
        Perform comprehensive data validation checks.
        Ensures data consistency, accuracy, completeness, and validity.
        """
        if self.data is None:
            raise ValueError("No data to validate. Please ingest data first.")

        # Check for null values
        if self.data.isnull().values.any():
            raise ValueError("Data contains null values.")

        # Check for duplicates
        if self.data.duplicated().any():
            raise ValueError("Data contains duplicate entries.")

        for field in required_fields:
            if field not in self.data.columns:
                raise ValueError(f"Missing required field: {field}")

        for field, expected_type in expected_types.items():
            if not np.issubdtype(self.data[field].dtype, np.dtype(expected_type)):
                raise ValueError(f"Field {field} does not have expected type {expected_type}.")        # Additional validation checks can be added here        # Additional checks can be added here
        print("Data validation completed successfully.")

    def transform_data(self, transformations):
        """
        Apply transformation rules to the data.
        Users can define rules such as changing data types, rearranging columns, etc.
        """
        if self.data is None:
            raise ValueError("No data to transform. Please ingest and validate data first.")

        for transformation in transformations:
            if transformation['type'] == 'rename':
                self.data.rename(columns=transformation['columns'], inplace=True)
            elif transformation['type'] == 'drop_duplicates':
                self.data.drop_duplicates(inplace=True)
            elif transformation['type'] == 'change_dtype':
                self.data[transformation['column']] = self.data[transformation['column']].astype(transformation['dtype'])
            # Additional transformation rules can be added here

        print("Data transformation completed successfully.")

    def export_data(self, destination, file_type):
        """
        Export the processed data to various formats (CSV, Excel).
        """
        if self.data is None:
            raise ValueError("No data to export. Please ingest, validate, and transform data first.")

        if file_type == 'csv':
            self.data.to_csv(destination, index=False)
        elif file_type == 'excel':
            self.data.to_excel(destination, index=False)
        else:
            raise ValueError("Unsupported file type. Use 'csv' or 'excel'.")

        print("Data export completed successfully.")

    def run_pipeline(self, source, file_type, transformations, export_destination, export_type):
        """
        Run the entire data processing pipeline: ingestion, validation, transformation, and export.
        Ensures the correct order of operations.
        """
        self.ingest_data(source, file_type)
        self.validate_data()
        self.transform_data(transformations)
        self.export_data(export_destination, export_type)

# Example usage:
if __name__ == "__main__":
    coordinator = DataFlowCoordinator()
    
    # Define transformations
    transformations = [
        {'type': 'rename', 'columns': {'old_name': 'new_name'}},
        {'type': 'drop_duplicates'},
        {'type': 'change_dtype', 'column': 'new_name', 'dtype': 'str'}
    ]
    
    # Run the data processing pipeline
    coordinator.run_pipeline('data.csv', 'csv', transformations, 'output.xlsx', 'excel')