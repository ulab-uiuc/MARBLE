# data_analyst_collaborator.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import json
import xlsxwriter
import csv

class Data_Analyst_Collaborator:
    def __init__(self):
        self.datasets = {}
        self.collaborators = {}
        self.changes_history = {}

    def import_dataset(self, name, file_path, file_type):
        """
        Import a dataset from a file.

        Args:
            name (str): The name of the dataset.
            file_path (str): The path to the file.
            file_type (str): The type of the file (CSV, Excel, JSON).

        Returns:
            None
        """
        if file_type == 'CSV':
            self.datasets[name] = pd.read_csv(file_path)
        elif file_type == 'Excel':
            self.datasets[name] = pd.read_excel(file_path)
        elif file_type == 'JSON':
            with open(file_path, 'r') as f:
                self.datasets[name] = pd.json_normalize(json.load(f))
        else:
            print("Unsupported file type.")

    def data_profiling(self, dataset_name):def merge_datasets(self, dataset1_name, dataset2_name, common_field, merge_type):def data_profiling(self, dataset_name):
    dataset = self.datasets[dataset_name]
    print("Data Types:")
    print(dataset.dtypes)
    print("\nMissing Values:")
    print(dataset.isnull().sum())
    print("\nSummary Statistics:")
    print(dataset.describe())
    plt.figure(figsize=(10, 8))
    sns.pairplot(dataset)
    plt.show()def correlation_analysis(self, dataset_name, variables):
        """
        Perform correlation analysis on a dataset.

        Args:
            dataset_name (str): The name of the dataset.
            variables (list): The variables to analyze.

        Returns:
            None
        """
        dataset = self.datasets[dataset_name]
        correlation_matrix = dataset[variables].corr()
        print("Correlation Matrix:")
        print(correlation_matrix)
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.show()

    def add_collaborator(self, name):
        """
        Add a collaborator to the project.

        Args:
            name (str): The name of the collaborator.

        Returns:
            None
        """
        self.collaborators[name] = []

    def add_change(self, collaborator_name, change):
        """
        Add a change to the changes history.

        Args:
            collaborator_name (str): The name of the collaborator.
            change (str): The change made.

        Returns:
            None
        """
        if collaborator_name in self.collaborators:
            self.collaborators[collaborator_name].append(change)
        else:
            print("Collaborator not found.")

    def view_changes_history(self):
        """
        View the changes history.

        Returns:
            None
        """
        for collaborator, changes in self.collaborators.items():
            print(f"Collaborator: {collaborator}")
            for change in changes:
                print(f"- {change}")

# Example usage
data_analyst_collaborator = Data_Analyst_Collaborator()

# Import datasets
data_analyst_collaborator.import_dataset('dataset1', 'dataset1.csv', 'CSV')
data_analyst_collaborator.import_dataset('dataset2', 'dataset2.xlsx', 'Excel')

# Perform data profiling
data_analyst_collaborator.data_profiling('dataset1')

# Merge datasets
data_analyst_collaborator.merge_datasets('dataset1', 'dataset2', 'common_field')

# Perform correlation analysis
data_analyst_collaborator.correlation_analysis('dataset1_dataset2', ['variable1', 'variable2'])

# Add collaborators
data_analyst_collaborator.add_collaborator('Collaborator1')
data_analyst_collaborator.add_collaborator('Collaborator2')

# Add changes
data_analyst_collaborator.add_change('Collaborator1', 'Added new dataset')
data_analyst_collaborator.add_change('Collaborator2', 'Updated correlation analysis')

# View changes history
data_analyst_collaborator.view_changes_history()