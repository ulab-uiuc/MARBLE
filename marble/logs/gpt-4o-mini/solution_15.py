# solution.py

import pandas as pd
import numpy as np

class DataFlowCoordinator:
    def __init__(self):
        self.data = None  # Placeholder for the data being processed

    def ingest_data(self, source, file_type):
        """
        Ingest data from various sources such as CSV, Excel, and databases.
        Validates the data format upon ingestion.
        """
        if file_type == 'csv':
            self.data = pd.read_csv(source)
        elif file_type == 'excel':
            self.data = pd.read_excel(source)
        else:
            raise ValueError("Unsupported file type. Please use 'csv' or 'excel'.")

        # Validate the data format after ingestion
        if self.data.empty:
            raise ValueError("Ingested data is empty. Please check the source.")

    def validate_data(self):
        """
        Perform comprehensive data validation checks for consistency, accuracy,
        completeness, and validity.
        """
        if self.data is None:
            raise ValueError("No data to validate. Please ingest data first.")        # Check for missing values
        if self.data.isnull().values.any():
            raise ValueError("Data contains missing values.")

        # Check for duplicates
        if self.data.duplicated().any():
            raise ValueError("Data contains duplicate entries.")

        # Check for required columns
        required_columns = ['name', 'age', 'email']
        for column in required_columns:
            if column not in self.data.columns:
                raise ValueError(f"Missing required column: {column}")

        # Check for out-of-range values
        if (self.data['age'] < 0).any():
            raise ValueError("Age cannot be negative.")

        # Check data types
        if not np.issubdtype(self.data['age'].dtype, np.integer):
            raise ValueError("Age must be an integer.")

        print("Data validation passed.")
        # Check for duplicates
        if self.data.duplicated().any():
            raise ValueError("Data contains duplicate entries.")

        # Additional validation checks can be added here
        print("Data validation passed.")

    def transform_data(self, transformations):
        """
        Apply transformation rules to the data, such as changing data types,
        rearranging columns, removing duplicates, and merging cells.
        """
        if self.data is None:
            raise ValueError("No data to transform. Please ingest and validate data first.")

        for transformation in transformations:
            if transformation['type'] == 'change_type':
                self.data[transformation['column']] = self.data[transformation['column']].astype(transformation['new_type'])
            elif transformation['type'] == 'remove_duplicates':
                self.data = self.data.drop_duplicates()
            elif transformation['type'] == 'rearrange_columns':
                self.data = self.data[transformation['new_order']]
            # Additional transformation rules can be added here

        print("Data transformation completed.")

    def export_data(self, destination, file_type):
        """
        Export the processed data to various formats, including CSV and Excel.
        """
        if self.data is None:
            raise ValueError("No data to export. Please ensure data is processed.")

        if file_type == 'csv':
            self.data.to_csv(destination, index=False)
        elif file_type == 'excel':
            self.data.to_excel(destination, index=False)
        else:
            raise ValueError("Unsupported file type. Please use 'csv' or 'excel'.")

        print(f"Data exported successfully to {destination}.")

# Example usage of the DataFlowCoordinator
if __name__ == "__main__":
    coordinator = DataFlowCoordinator()

    # Step 1: Ingest data
    coordinator.ingest_data('data.csv', 'csv')

    # Step 2: Validate data
    coordinator.validate_data()

    # Step 3: Transform data
    transformations = [
        {'type': 'change_type', 'column': 'age', 'new_type': 'int'},
        {'type': 'remove_duplicates'},
        {'type': 'rearrange_columns', 'new_order': ['name', 'age', 'email']}
    ]
    coordinator.transform_data(transformations)

    # Step 4: Export data
    coordinator.export_data('processed_data.csv', 'csv')