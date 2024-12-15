# for editing yaml
import yaml
import copy
import os

# Add custom representers for block style strings
class folded_str(str): pass
class literal_str(str): pass

def folded_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')
def literal_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(folded_str, folded_str_representer)
yaml.add_representer(literal_str, literal_str_representer)

model_names_short_full = {
    'gpt-3.5-turbo': 'gpt-3.5-turbo',
    'gpt-4o-mini': 'gpt-4o-mini',
    'llama-3.1-8b': 'together_ai/meta-llama/Llama-3.1-8B-Instruct',
    'llama-3.1-70b': 'together_ai/meta-llama/Llama-3.1-70B-Instruct',
    'llama-3.3-70b': 'together_ai/meta-llama/Llama-3.3-70B-Instruct',
}

scenarios = [
    "E_COMMERCE",
    "EDUCATION",
    "FILE_SHARING",
    "FINANCE",
    "HEALTHCARE",
    "INTERNET_OF_THINGS",
    "SOCIAL_MEDIA",
    "MUSIC_STREAMING",
    "MANUFACTURING",
    "TRANSPORTATION",
]


descriptions = {
    'E_COMMERCE': 'This database is used in an e-commerce system to manage customer information, product details, orders, order items, and payments. It consists of five main tables: customers, products, orders, order items, and payments, with foreign key relationships between them.',
    'EDUCATION': 'This database is used in an educational system to manage student, course, enrollment, and payment information. It consists of four tables: students, courses, enrollments, and payments.',
    'FILE_SHARING': 'This database is used in a File Sharing System to manage users, files, file sharing, and file access logs. It consists of four main tables: users, files, shared_files, and file_access_logs.',
    'FINANCE': 'This database is used for managing financial data within a Finance Management System. It tracks users, their accounts, transactions, investments, and investment transactions.',
    'HEALTHCARE': 'This database is used in a healthcare management system to track and manage patient information, doctor details, appointments, medical records, and treatments.',
    'INTERNET_OF_THINGS': 'This database is used for an IoT (Internet of Things) system where various devices collect and manage data. It includes tables to store device details, user information, collected data, logs, configurations, alerts, device statuses, and commands.',
    'SOCIAL_MEDIA': 'This database is used for a Social Media platform, where users can create posts, comment on posts, like posts, follow other users, send direct messages, and upload media. The schema covers key aspects such as user information, social interactions (like, comments, follow), messaging, and media management.',
    'MUSIC_STREAMING': 'This database is used for a Music Streaming platform where users can listen to songs, create playlists, track their listening activity, and subscribe to premium services. The schema includes tables for users, artists, albums, songs, playlists, and subscription details. It also tracks user activities and payments.',
    'MANUFACTURING': 'This database is used for a Manufacturing system that tracks customers, products, suppliers, orders, inventory, raw materials, manufacturing orders, and payments. It includes relationships between orders, manufacturing, and inventory management to ensure smooth manufacturing operations.',
    'TRANSPORTATION': 'This database schema covers multiple aspects of a transportation system, including vehicles, drivers, routes, trips, cargo, maintenance, fuel logs, and payments. It allows efficient tracking of trips, vehicle statuses, and associated payments, ensuring smooth operations in a transportation company.'
}

# load all yamls starting with BASE_
file_list = os.listdir()

# make dir as shorts for model names
for model_name in model_names_short_full.keys():
    folder_name = f"test_config_db_{model_name}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# make the result_{model_name} folder
for model_name in model_names_short_full.keys():
    folder_name = f"result_{model_name}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

for file in file_list:
    if file.startswith("BASE_"):
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        # edit data
        # get .task.content
        task_content = copy.deepcopy(data["task"]["content"])
        anomalies = copy.deepcopy(data["environment"]["anomalies"])
        # get file content from scenario.lower.yaml
        file_path = data["output"]["file_path"]
        print(f"Anomalies: {anomalies}")
        for scenario in scenarios:
            with open(scenario.lower() + ".sql", 'r', encoding='utf-8') as f:
                scenario_data = f.read()
            # edit envionment.init_sql
            data["environment"]["init_sql"] = scenario_data
            scenario_desc = descriptions[scenario]
            data["task"]["content"] = scenario_desc + "\n" + task_content
            # replace BASE_ in .output.file_path
            # replace BASE_ in file name to save
            new_file = copy.deepcopy(file)
            new_file = new_file.replace("BASE_", scenario + "_")
            for model_name in model_names_short_full.keys():
                anomalies__ = copy.deepcopy(anomalies)
                data["output"]["file_path"] = file_path.replace("BASE_", scenario + "_").replace("result/", f"result/result_{model_name}/")
                model_full_name = model_names_short_full[model_name]
                data["llm"] = model_full_name
                data["environment"]["anomalies"] = anomalies__
                with open(f"test_config_db_{model_name}/{new_file}", 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            # with open(new_file, 'w', encoding='utf-8') as f:
            #     # use | to do multiline string
            #     yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# # In the main processing loop, convert strings to literal_str
# for file in file_list:
#     if file.startswith("BASE_"):
#         with open(file, 'r', encoding='utf-8') as f:
#             data = yaml.safe_load(f)
        
#         def iter_make_literal_str(data):
#             for key, value in data.items():
#                 if isinstance(value, dict):
#                     iter_make_literal_str(value)
#                 elif isinstance(value, str):
#                     data[key] = literal_str(value)
#             return data

#         data = iter_make_literal_str(data)
            
#         task_content = copy.deepcopy(data["task"]["content"])
#         file_path = data["output"]["file_path"]
        
#         for scenario in scenarios:
#             with open(scenario.lower() + ".sql", 'r', encoding='utf-8') as f:
#                 scenario_data = f.read()
            
#             scenario_desc = descriptions[scenario]
#             # Convert SQL and content to literal string style
#             data["environment"]["init_sql"] = literal_str(scenario_data)
#             data["task"]["content"] = literal_str(scenario_desc + "\n\n" + task_content)
#             file_path_ = copy.deepcopy(file_path)
#             data["output"]["file_path"] = file_path_.replace("BASE_", scenario + "_").replace("result/", f"result/result_{model_name}/")
            
#             new_file = file.replace("BASE_", scenario + "_")
            
#             for model_name in model_names_short_full.keys():
#                 model_full_name = model_names_short_full[model_name]
#                 data["llm"] = model_full_name
#                 with open(f"test_config_db_{model_name}/{new_file}", 'w', encoding='utf-8') as f:
#                     yaml.dump(data, f, default_flow_style=False, sort_keys=False)
