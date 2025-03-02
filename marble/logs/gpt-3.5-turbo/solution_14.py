# solution.py

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to import datasets in various formats (CSV, Excel, JSON)
def import_dataset(file_path, file_format):
    if file_format == 'csv':
        return pd.read_csv(file_path)
    elif file_format == 'excel':
        return pd.read_excel(file_path)
    elif file_format == 'json':
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide CSV, Excel, or JSON.")

# Function for data profiling
def data_profiling(data):
    # Automatic detection of data types
    data_types = data.dtypes
    
    # Identification of missing values
    missing_values = data.isnull().sum()
    
    # Generation of summary statistics
    summary_statistics = data.describe()
    
    # Generate visualizations
    for column in data.columns:
        if data[column].dtype in ['int64', 'float64']:
            plt.figure(figsize=(6, 4))
            sns.histplot(data[column].dropna(), kde=True)
            plt.title(f'{column} Distribution')
            plt.show()

# Function to merge datasets based on common fields
def merge_datasets(data1, data2, how='inner', on=None):
    return pd.merge(data1, data2, how=how, on=on)

# Function for correlation analysis
def correlation_analysis(data, method='pearson'):
    correlation_matrix = data.corr(method=method)
    
    # Visualize correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Correlation Matrix ({method.capitalize()} Correlation)')
    plt.show()

# Main function to demonstrate the functionality
def main():
    # Import datasets
    data1 = import_dataset('data1.csv', 'csv')
    data2 = import_dataset('data2.xlsx', 'excel')
    
    # Data profiling
    data_profiling(data1)
    
    # Merge datasets
    merged_data = merge_datasets(data1, data2, how='inner', on='common_field')
    
    # Correlation analysis
    correlation_analysis(merged_data, method='pearson')

# Execute the main function
if __name__ == "__main__":
    main()