import json
import random

# Define the file paths for the two JSON files and the output file
file1_path = './paper_bench_easy_500.json'  # JSON file with the detailed paper_data entries
file2_path = './research_town_data/paper_bench_easy.json'  # JSON file from which we randomly choose keys
output_path = './researchtown_json/randomly_select_easy_33.json'  # Output file where the selected entries from file1 will be saved

# Open and load the first JSON file
with open(file1_path, 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

# Open and load the second JSON file
with open(file2_path, 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)

# Get all keys from the second JSON file
keys_file2 = list(data2.keys())

# Randomly choose 34 keys from file2's keys
# If the total number of keys is less than 34, this will raise a ValueError.
# You might want to add error handling if this case is possible.
selected_keys = random.sample(keys_file2, 50)

# Initialize an empty dictionary to hold the selected entries from file1
selected_data = {}

# Loop over the selected keys and get the corresponding entry from data1 if it exists
count = 0
for key in selected_keys:
    if key in data1:
        selected_data[key] = data1[key]
        count += 1
        if count == 33:
            break
    else:
        # Optionally, handle the case where the key is not found in data1.
        # For example, you could print a warning message.
        print(f"Warning: Key {key} not found in the first JSON file.")

# Write the selected data to the output JSON file
with open(output_path, 'w', encoding='utf-8') as out_file:
    json.dump(selected_data, out_file, ensure_ascii=False, indent=4)

print(f"Selected data for {len(selected_data)} entries has been written to {output_path}.")
