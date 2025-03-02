# solution.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mutual_info_score
from scipy.stats import pearsonr, spearmanr
import json
import openpyxl
from openpyxl import load_workbook
from threading import Thread
import time

class Data_Analyst_Collaborator:
    def __init__(self):
        self.datasets = {}
        self.current_dataset = None
        self.collaborators = []

    def import_dataset(self, file_path, file_format):
        if file_format == 'csv':
            self.datasets[file_path] = pd.read_csv(file_path)
        elif file_format == 'excel':
            self.datasets[file_path] = pd.read_excel(file_path)
        elif file_format == 'json':
            self.datasets[file_path] = pd.read_json(file_path)
        else:
            print("Unsupported file format")

    def profile_dataset(self, dataset):
        print("Data Types:")
        print(dataset.dtypes)
        print("Missing Values:")
        print(dataset.isnull().sum())
        print("Summary Statistics:")
        print(dataset.describe())
        plt.figure(figsize=(10, 6))
        dataset.hist()
        plt.show()

    def merge_datasets(self, dataset1, dataset2, merge_type):
        if merge_type == 'horizontal':
            self.current_dataset = pd.merge(dataset1, dataset2, how='outer', on='key')
        elif merge_type == 'vertical':
            self.current_dataset = pd.merge(dataset1, dataset2, how='outer', left_index=True, right_index=True)
        else:
            print("Unsupported merge type")

    def correlation_analysis(self, dataset, variables):
        pearson_corr = pearsonr(dataset[variables[0]], dataset[variables[1]])
        spearman_corr = spearmanr(dataset[variables[0]], dataset[variables[1]])
        print(f"Pearson Correlation: {pearson_corr[0]}")
        print(f"Spearman Correlation: {spearman_corr[0]}")
        plt.figure(figsize=(8, 6))
        plt.scatter(dataset[variables[0]], dataset[variables[1]])
        plt.xlabel(variables[0])
        plt.ylabel(variables[1])
        plt.show()

    def collaborate(self, collaborator):
        self.collaborators.append(collaborator)
        print(f"Collaborator {collaborator} joined the session")

    def update_dataset(self, dataset):
        self.current_dataset = dataset
        print("Dataset updated")

    def version_control(self):
        print("Version Control:")
        for file_path in self.datasets:
            print(f"File: {file_path}")
            print(f"Version: {self.datasets[file_path].shape}")

def main():
    data_analyst = Data_Analyst_Collaborator()

    # Import datasets
    data_analyst.import_dataset('data1.csv', 'csv')
    data_analyst.import_dataset('data2.xlsx', 'excel')
    data_analyst.import_dataset('data3.json', 'json')

    # Profile datasets
    data_analyst.profile_dataset(data_analyst.datasets['data1.csv'])
    data_analyst.profile_dataset(data_analyst.datasets['data2.xlsx'])
    data_analyst.profile_dataset(data_analyst.datasets['data3.json'])

    # Merge datasets
    data_analyst.merge_datasets(data_analyst.datasets['data1.csv'], data_analyst.datasets['data2.xlsx'], 'horizontal')

    # Correlation analysis
    data_analyst.correlation_analysis(data_analyst.current_dataset, ['variable1', 'variable2'])

    # Collaborate
    data_analyst.collaborate('Collaborator 1')
    data_analyst.collaborate('Collaborator 2')

    # Update dataset
    data_analyst.update_dataset(data_analyst.current_dataset)

    # Version control
    data_analyst.version_control()

if __name__ == "__main__":
    main()