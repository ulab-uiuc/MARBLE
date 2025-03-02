# solution.py

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any

class Data_Analyst_Collaborator:
    def __init__(self):
        """Initialize the Data Analyst Collaborator with an empty dataset list and history."""
        self.datasets = []
        self.history = []

    def import_data(self, file_path: str) -> pd.DataFrame:
        """Import datasets from various formats (CSV, Excel, JSON).
        
        Args:
            file_path (str): The path to the dataset file.
        
        Returns:
            pd.DataFrame: The imported dataset as a DataFrame.
        """
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            data = pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV, Excel, or JSON.")
        
        self.datasets.append(data)
        self.history.append(f"Imported data from {file_path}")
        return data

    def data_profiling(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Perform data profiling on the given DataFrame.
        
        Args:
            data (pd.DataFrame): The DataFrame to profile.
        
        Returns:
            Dict[str, Any]: A dictionary containing profiling results.
        """
        profiling_info = {
            'data_types': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'summary_statistics': data.describe(include='all').to_dict()
        }
        return profiling_info

    def merge_datasets(self, data1: pd.DataFrame, data2: pd.DataFrame, on: str, how: str = 'inner') -> pd.DataFrame:
        """Merge two datasets based on a common field.
        
        Args:
            data1 (pd.DataFrame): The first DataFrame.
            data2 (pd.DataFrame): The second DataFrame.
            on (str): The column name to merge on.
            how (str): The type of merge to perform (inner, outer, left, right).
        
        Returns:
            pd.DataFrame: The merged DataFrame.
        """
    def correlation_analysis(self, data: pd.DataFrame, columns: List[str], method: str = 'pearson') -> pd.DataFrame:
        """Calculate correlation coefficients between selected variables.
        
        Args:
            data (pd.DataFrame): The DataFrame to analyze.
            columns (List[str]): The list of columns to analyze.
            method (str): The correlation method to use ('pearson' or 'spearman').
        
        Returns:
            pd.DataFrame: A DataFrame containing correlation coefficients.
        """
        correlation_matrix = data[columns].corr(method=method)
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')        plt.title('Correlation Matrix')
        plt.show()
        return correlation_matrix

    def scatter_plot(self, data: pd.DataFrame, x: str, y: str) -> None:
        """Create a scatter plot for two variables.
        
        Args:
            data (pd.DataFrame): The DataFrame containing the data.
            x (str): The column name for the x-axis.
            y (str): The column name for the y-axis.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=x, y=y)
        plt.title(f'Scatter Plot of {x} vs {y}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def add_annotation(self, annotation: str) -> None:
        """Add an annotation to the history.
        
        Args:
            annotation (str): The annotation to add.
        """
        self.history.append(annotation)

    def get_history(self) -> List[str]:
        """Get the history of actions performed.
        
        Returns:
            List[str]: A list of history entries.
        """
        return self.history

# Example usage:
if __name__ == "__main__":
    collaborator = Data_Analyst_Collaborator()
    # Import datasets
    df1 = collaborator.import_data('data1.csv')
    df2 = collaborator.import_data('data2.xlsx')
    
    # Data profiling
    profile1 = collaborator.data_profiling(df1)
    print("Profile of Data1:", profile1)
    
    # Merge datasets
    merged_df = collaborator.merge_datasets(df1, df2, on='common_column', how='inner')
    
    # Correlation analysis
    correlation_matrix = collaborator.correlation_analysis(merged_df, columns=['var1', 'var2', 'var3'])
    
    # Scatter plot
    collaborator.scatter_plot(merged_df, x='var1', y='var2')
    
    # Get history
    print("Action History:", collaborator.get_history())