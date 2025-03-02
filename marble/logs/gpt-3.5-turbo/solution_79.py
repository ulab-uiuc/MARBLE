# Multi-Agent City Planner Simulation

class Agent:
    def __init__(self, role):
        self.role = role

    def communicate(self, message):
        print(f"{self.role} received message: {message}")

    def collaborate(self, decision):
        print(f"{self.role} collaborated on decision: {decision}")

class CityPlannerAgent(Agent):
    def __init__(self):
        super().__init__("Urban Planner")

    def plan_city_layout(self):
        return "City layout planned"

class ResourceManagerAgent(Agent):
        print(f'{self.role} communicated: {message}')
        print(f'{self.role} collaborated on decision: {decision}')
    def __init__(self):
        super().__init__("Resource Manager")

    def allocate_resources(self):
        return "Resources allocated"
        print(f'{self.role} collaborated on decision: {decision}')
        print(f'{self.role} communicated: {message}')

class ConstructionSupervisorAgent(Agent):
    def __init__(self):
        super().__init__("Construction Supervisor")

    def manage_construction(self):
        return "Construction managed"

class PublicServiceCoordinatorAgent(Agent):
    def __init__(self):
        super().__init__("Public Service Coordinator")

    def ensure_well_being(self):
        return "Well-being ensured"

# Simulation
urban_planner = CityPlannerAgent()
resource_manager = ResourceManagerAgent()
construction_supervisor = ConstructionSupervisorAgent()
public_service_coordinator = PublicServiceCoordinatorAgent()

# Communication and Collaboration
urban_planner.communicate("Need resources for city layout planning")
resource_manager.communicate("Received request for resources")
decision = resource_manager.allocate_resources()
urban_planner.collaborate(decision)

construction_supervisor.communicate("Ready to start construction")
decision = construction_supervisor.manage_construction()
urban_planner.collaborate(decision)

public_service_coordinator.communicate("City services operational")
decision = public_service_coordinator.ensure_well_being()
urban_planner.collaborate(decision)