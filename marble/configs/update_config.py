# to yaml files in the following folders:
# test_config_db_gpt-3.5-turbo
# test_config_db_gpt-4o-mini
# test_config_db_llama-3.1-8b
# test_config_db_llama-3.1-70b
# test_config_db_llama-3.3-70b

origiinal = """    Recently, during operation, the database has seen performance issues. Use sql
    queries to find out what is wrong, and find out the reason that caused it. The
    root cause can be only two of the following: ''INSERT_LARGE_DATA'', ''MISSING_INDEXES'',
    ''LOCK_CONTENTION'', ''VACUUM'', ''REDUNDANT_INDEX'', ''FETCH_LARGE_DATA''. The
    planner should assign different agent to analyze possbility for each root cause
    and make final decision. Agents can also chat with each other to share information.  Please
    make the decision after using all these tools, as a premature decision may lead
    to incorrect conclusions. If the last round involves the Agents investigating
    via SQL queries, the next round should allow them to communicate to each other
    and discuss. In this round, each agent could talk to one other agent. Otherwise,
    assign the agents to investigate these reasons - agent1 on ''INSERT_LARGE_DATA'',
    agent 2 on ''MISSING_INDEXES'', ..., agent5 on ''FETCH_LARGE_DATA''.
"""
replacement = """    Recently, during operation, the database has seen performance issues. Use sql
    queries to find out what is wrong, and find out the reason that caused it. The
    root cause can be only two of the following: ''INSERT_LARGE_DATA'', ''MISSING_INDEXES'',
    ''LOCK_CONTENTION'', ''VACUUM'', ''REDUNDANT_INDEX'', ''FETCH_LARGE_DATA'', ''POOR_JOIN_PERFORMANCE,CPU_CONTENTION''.
    The planner should assign different agent to analyze possbility for each root
    cause and make final decision. Agents can also chat with each other to share information.  Please
    make the decision after using all these tools, as a premature decision may lead
    to incorrect conclusions.
"""
original_2 = "max_iterations: 10"
replacement_2 = "max_iterations: 5"

original_3 = "number_of_labels_pred: 2"
replacement_3 = "number_of_labels_pred: 3"

original_4 = "two"
replacement_4 = "three"

import os

folders = [
    'test_config_db_gpt-3.5-turbo',
    'test_config_db_gpt-4o-mini',
    'test_config_db_llama-3.1-8b',
    'test_config_db_llama-3.1-70b',
    'test_config_db_llama-3.3-70b'
]

single_files = os.listdir("../configs_v1/test_config_db_gpt-3.5-turbo")
x=0
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith('.yaml'):
            # remove if file is in "../confifs_v1/test_config_db_gpt-3.5-turbo" and ends with ".yaml"
            if file in single_files:
                os.remove(os.path.join(folder, file))
                continue

            with open(os.path.join(folder, file), 'r') as f:
                data = f.read()
            data = data.replace(origiinal, replacement)

            data = data.replace(original_2, replacement_2)

            data = data.replace(original_3, replacement_3)

            data = data.replace(original_4, replacement_4)

            with open(os.path.join(folder, file), 'w') as f:
                f.write(data)
print(x)