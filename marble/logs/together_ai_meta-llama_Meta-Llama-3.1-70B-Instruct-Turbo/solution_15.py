# data_ingestion_module.py
import pandas as pd
import sqlite3

class DataIngestionModule:
    """
    Module to ingest data from various sources such as CSV, Excel, and database connections.
    """
    
    def __init__(self):
        self.data = None

    def ingest_from_csv(self, file_path):
        """
        Ingest data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file.
        """
        try:
            self.data = pd.read_csv(file_path)
            print("Data ingested successfully from CSV file.")
        except Exception as e:
            print(f"Error ingesting data from CSV file: {e}")

    def ingest_from_excel(self, file_path):
        """
        Ingest data from an Excel file.
        
        Args:
            file_path (str): Path to the Excel file.
        """
        try:
            self.data = pd.read_excel(file_path)
            print("Data ingested successfully from Excel file.")
        except Exception as e:
            print(f"Error ingesting data from Excel file: {e}")

    def ingest_from_database(self, db_path, query):
        """
        Ingest data from a database.
        
        Args:
            db_path (str): Path to the database file.
            query (str): SQL query to execute.
        """
        try:
            conn = sqlite3.connect(db_path)
            self.data = pd.read_sql_query(query, conn)
            conn.close()
            print("Data ingested successfully from database.")
        except Exception as e:
            print(f"Error ingesting data from database: {e}")

    def get_data(self):
        """
        Get the ingested data.
        
        Returns:
            pandas.DataFrame: The ingested data.
        """
        return self.data


# data_validation_module.py
import pandas as pd

class DataValidationModule:
    """
    Module to perform comprehensive data validation.
    """
    
    def __init__(self, data):
        self.data = data

    def validate_data(self):
        """
        Validate the data for consistency, accuracy, completeness, and validity.
        """
        try:
            # Check for missing values
            if self.data.isnull().values.any():
                print("Data contains missing values.")
                return False

            # Check for duplicate rows
            if self.data.duplicated().any():
                print("Data contains duplicate rows.")
                return False

            # Check for invalid data types
            for column in self.data.columns:
                if self.data[column].dtype not in ['int64', 'float64', 'object']:
                    print(f"Invalid data type in column {column}.")
                    return False

            print("Data is valid.")
            return True
        except Exception as e:
            print(f"Error validating data: {e}")
            return False


# data_transformation_module.py
import pandas as pd

class DataTransformationModule:
    """
    Module to apply transformation rules to the data.
    """
    
    def __init__(self, data):
        self.data = data

    def transform_data(self, transformation_rules):
        """
        Apply transformation rules to the data.
        
        Args:
            transformation_rules (dict): Dictionary of transformation rules.
        """
        try:
            for rule in transformation_rules:
                if rule == 'change_data_type':
                    for column, data_type in transformation_rules[rule].items():
                        self.data[column] = self.data[column].astype(data_type)
                elif rule == 'rearrange_columns':
                    self.data = self.data[transformation_rules[rule]]
                elif rule == 'remove_duplicates':
                    self.data = self.data.drop_duplicates()
                elif rule == 'merge_cells':
                    for column in transformation_rules[rule]:
                        self.data[column] = self.data[column].fillna('')

            print("Data transformed successfully.")
        except Exception as e:
            print(f"Error transforming data: {e}")

    def get_transformed_data(self):
        """
        Get the transformed data.
        
        Returns:
            pandas.DataFrame: The transformed data.
        """
        return self.data


# data_export_module.py
import pandas as pd
import sqlite3

class DataExportModule:
    """
    Module to export the processed data to various formats.
    """
    
    def __init__(self, data):
        self.data = data

    def export_to_csv(self, file_path):
        """
        Export data to a CSV file.
        
        Args:
            file_path (str): Path to the CSV file.
        """
        try:
            self.data.to_csv(file_path, index=False)
            print("Data exported successfully to CSV file.")
        except Exception as e:
            print(f"Error exporting data to CSV file: {e}")

    def export_to_excel(self, file_path):
        """
        Export data to an Excel file.
        
        Args:
            file_path (str): Path to the Excel file.
        """
        try:
            self.data.to_excel(file_path, index=False)
            print("Data exported successfully to Excel file.")
        except Exception as e:
            print(f"Error exporting data to Excel file: {e}")

    def export_to_database(self, db_path, table_name):
        """
        Export data to a database.
        
        Args:
            db_path (str): Path to the database file.
            table_name (str): Name of the table to export to.
        """
        try:
            conn = sqlite3.connect(db_path)
            self.data.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            print("Data exported successfully to database.")
        except Exception as e:
            print(f"Error exporting data to database: {e}")


# data_flow_coordinator.py
class DataFlowCoordinator:
    """
    Class to manage and coordinate the processing of data through multiple stages.
    """
    
    def __init__(self):
        self.data_ingestion_module = DataIngestionModule()
        self.data_validation_module = None
        self.data_transformation_module = None
        self.data_export_module = None

    def ingest_data(self, source, file_path=None, query=None):
        """
        Ingest data from a source.
        
        Args:
            source (str): Source of the data (CSV, Excel, database).
            file_path (str): Path to the file (if applicable).
            query (str): SQL query to execute (if applicable).
        """
        if source == 'CSV':
            self.data_ingestion_module.ingest_from_csv(file_path)
        elif source == 'Excel':
            self.data_ingestion_module.ingest_from_excel(file_path)
        elif source == 'database':
            self.data_ingestion_module.ingest_from_database(file_path, query)

    def validate_data(self):
        """
        Validate the ingested data.
        """
        self.data_validation_module = DataValidationModule(self.data_ingestion_module.get_data())
        if not self.data_validation_module.validate_data():
            print("Data is invalid. Cannot proceed with processing.")
            return False
        return True

    def transform_data(self, transformation_rules):
        """
        Transform the validated data.
        
        Args:
            transformation_rules (dict): Dictionary of transformation rules.
        """
        self.data_transformation_module = DataTransformationModule(self.data_ingestion_module.get_data())
        self.data_transformation_module.transform_data(transformation_rules)

    def export_data(self, destination, file_path=None, table_name=None):
        """
        Export the transformed data to a destination.
        
        Args:
            destination (str): Destination of the data (CSV, Excel, database).
            file_path (str): Path to the file (if applicable).
            table_name (str): Name of the table to export to (if applicable).
        """
        self.data_export_module = DataExportModule(self.data_transformation_module.get_transformed_data())
        if destination == 'CSV':
            self.data_export_module.export_to_csv(file_path)
        elif destination == 'Excel':
            self.data_export_module.export_to_excel(file_path)
        elif destination == 'database':
            self.data_export_module.export_to_database(file_path, table_name)


# solution.py
def main():
    data_flow_coordinator = DataFlowCoordinator()
    data_flow_coordinator.ingest_data('CSV', 'data.csv')
    if data_flow_coordinator.validate_data():
        transformation_rules = {
            'change_data_type': {'column1': 'int64', 'column2': 'float64'},
            'rearrange_columns': ['column1', 'column2', 'column3'],
            'remove_duplicates': True,
            'merge_cells': ['column1', 'column2']
        }
        data_flow_coordinator.transform_data(transformation_rules)
        data_flow_coordinator.export_data('Excel', 'output.xlsx')

if __name__ == "__main__":
    main()