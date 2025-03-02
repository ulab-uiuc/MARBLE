# solution.py
# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import correlation_matrix
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import json
import openpyxl
import os

# Data_Analyst_Collaborator class
class Data_Analyst_Collaborator:
    def __init__(self):
        self.datasets = {}
        self.current_dataset = None
        self.collaborators = []

    # Method to import datasets
    def import_dataset(self, dataset_name, file_path, file_format):
        if file_format == 'csv':
            self.datasets[dataset_name] = pd.read_csv(file_path)
        elif file_format == 'excel':
            self.datasets[dataset_name] = pd.read_excel(file_path)
        elif file_format == 'json':
            self.datasets[dataset_name] = pd.read_json(file_path)
        else:
            print("Unsupported file format")

    # Method to profile the dataset
    def profile_dataset(self, dataset_name):
        if dataset_name in self.datasets:
            self.current_dataset = self.datasets[dataset_name]
            print("Data Types:")
            print(self.current_dataset.dtypes)
            print("Missing Values:")
            print(self.current_dataset.isnull().sum())
            print("Summary Statistics:")
            print(self.current_dataset.describe())
            self.current_dataset.plot(kind='bar')
            plt.show()
        else:
            print("Dataset not found")

    # Method to merge datasets
    def merge_datasets(self, dataset1_name, dataset2_name, merge_type):
        if dataset1_name in self.datasets and dataset2_name in self.datasets:
            if merge_type == 'horizontal':
                self.datasets[dataset1_name] = pd.merge(self.datasets[dataset1_name], self.datasets[dataset2_name], how='outer')
            elif merge_type == 'vertical':
                self.datasets[dataset1_name] = pd.merge(self.datasets[dataset1_name], self.datasets[dataset2_name], how='inner')
            else:
                print("Unsupported merge type")
        else:
            print("One or both datasets not found")

    # Method to perform correlation analysis
    def correlation_analysis(self, dataset_name, variables):
        if dataset_name in self.datasets:
            self.current_dataset = self.datasets[dataset_name]
            correlation_matrix = self.current_dataset[variables].corr()
            print(correlation_matrix)
            plt.figure(figsize=(10, 8))
            plt.imshow(correlation_matrix, cmap='hot', interpolation='nearest')
            plt.show()
        else:
            print("Dataset not found")

    # Method to add collaborators
    def add_collaborator(self, collaborator_name):
        self.collaborators.append(collaborator_name)

    # Method to start collaboration
    def start_collaboration(self):
        print("Collaboration started")
        for collaborator in self.collaborators:
            print(f"{collaborator} joined the collaboration")

    # Method to update dataset
    def update_dataset(self, dataset_name, new_data):
        if dataset_name in self.datasets:
            self.datasets[dataset_name] = pd.concat([self.datasets[dataset_name], pd.DataFrame(new_data)], ignore_index=True)
        else:
            print("Dataset not found")

    # Method to save dataset
    def save_dataset(self, dataset_name, file_path, file_format):
        if dataset_name in self.datasets:
            if file_format == 'csv':
                self.datasets[dataset_name].to_csv(file_path, index=False)
            elif file_format == 'excel':
                self.datasets[dataset_name].to_excel(file_path, index=False)
            elif file_format == 'json':
                self.datasets[dataset_name].to_json(file_path, orient='records')
            else:
                print("Unsupported file format")
        else:
            print("Dataset not found")

# Main function
def main():
    collaborator = Data_Analyst_Collaborator()

    # Importing datasets
    collaborator.import_dataset('dataset1', 'data/dataset1.csv', 'csv')
    collaborator.import_dataset('dataset2', 'data/dataset2.csv', 'csv')

    # Profiling datasets
    collaborator.profile_dataset('dataset1')
    collaborator.profile_dataset('dataset2')

    # Merging datasets
    collaborator.merge_datasets('dataset1', 'dataset2', 'horizontal')

    # Performing correlation analysis
    collaborator.correlation_analysis('dataset1', ['variable1', 'variable2'])

    # Adding collaborators
    collaborator.add_collaborator('Collaborator1')
    collaborator.add_collaborator('Collaborator2')

    # Starting collaboration
    collaborator.start_collaboration()

    # Updating dataset
    new_data = {'variable1': [1, 2, 3], 'variable2': [4, 5, 6]}
    collaborator.update_dataset('dataset1', new_data)

    # Saving dataset
    collaborator.save_dataset('dataset1', 'data/dataset1_updated.csv', 'csv')

if __name__ == "__main__":
    main()