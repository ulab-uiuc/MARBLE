from diagnostic_kb import DiagnosticKB
# Initialize the knowledge base
kb = DiagnosticKB()

# Search for CPU-related issues

results = kb.search("slow query", expert='WorkloadExpert')

print(kb.get_experts())
for result in results:
    print(f"Cause : {result['cause_name']}")
    # print(f"Score: {result['score']}")
    print("Metrics:", result['metrics'])
    print("Expert :", result['expert'])
    # print("-" * 50)
    # print(result)

# Get all diagnostic causes
# all_causes = kb.get_all_causes()

# Get specific diagnostic
cpu_diagnostic = kb.get_diagnostic_by_cause("cpu_resource_contention")

# print(cpu_diagnostic)
