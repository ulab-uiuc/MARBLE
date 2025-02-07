# for each folder in this directory, read all yaml files as str
# replace max_iterations: 10 with max_iterations: 4

import os
import copy
import yaml

folders = os.listdir()

for folder in folders:
    if os.path.isdir(folder):
        files = os.listdir(folder)
        for file in files:
            if file.endswith(".yaml"):
                with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
                    data = f.read()
                data = data.replace("max_iterations: 10", "max_iterations: 4")
                with open(os.path.join(folder, file), 'w', encoding='utf-8') as f:
                    f.write(data)