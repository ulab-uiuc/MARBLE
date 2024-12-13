# for editing yaml
import yaml
import copy
import os

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

for file in file_list:
    if file.startswith("BASE_"):
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        # edit data
        # get .task.content
        task_content = copy.deepcopy(data["task"]["content"])
        # get file content from scenario.lower.yaml
        for scenario in scenarios:
            with open(scenario.lower() + ".sql", 'r', encoding='utf-8') as f:
                scenario_data = f.read()
            # edit envionment.init_sql
            data["environment"]["init_sql"] = scenario_data
            scenario_desc = descriptions[scenario]
            data["task"]["content"] = scenario_desc + "\n\n" + task_content
            # replace BASE_ in .output.file_path
            data["output"]["file_path"] = data["output"]["file_path"].replace("BASE_", scenario + "_")
            # replace BASE_ in file name to save
            new_file = copy.deepcopy(file)
            new_file = new_file.replace("BASE_", scenario + "_")
            with open(new_file, 'w', encoding='utf-8') as f:
                # use | to do multiline string
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
