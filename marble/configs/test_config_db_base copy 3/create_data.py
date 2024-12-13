# for editing yaml
import yaml
import copy
import os

scenarios = [
    "E_COMMERCE",
    "EDUCATION",
    # "FILE_SHARING",
    # "FINANCE",
    # "HEALTH_CARE",
    # "INTERNET_OF_THINGS",
    # "SOCIAL_MEDIA",
    # "MUSIC_STREAMING",
    # "MANUFACTURING",
    # "TRANSPORTATION",
]


descriptions = {
    'E_COMMERCE': 'This database is designed to manage an e-commerce system with functionalities for users, products, inventory, orders, and reviews. It tracks user information, including contact details, and stores products with descriptions, prices, and categories. The inventory table keeps track of stock levels for each product, while the orders and order_items tables handle customer orders and the products associated with them. Reviews are stored for products, allowing users to rate and leave feedback, and various queries provide insights into sales, inventory, and user activity.',
    'EDUCATION': 'The database is designed to manage educational information for a university, covering departments, faculty, courses, students, and research projects. It allows tracking of faculty members\' details, including their academic rank, research interests, and associated projects, along with the courses they teach. The students\' information, including their major, GPA, and course enrollments, is captured along with their performance metrics in various courses. It also includes detailed records of research projects, funding, and contributors, both faculty and students, enhancing the understanding of academic contributions. Finally, the system enables analytical queries such as student performance, course success rates, and faculty research impact, supporting educational insights and projections.',
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
