# solution.py

import random
import time
from threading import Thread, Lock

# Define a base class for agents
class Agent:
    def __init__(self, name):
        self.name = name
        self.communication_lock = Lock()

    def communicate(self, message):
        with self.communication_lock:
            print(f"{self.name} communicates: {message}")

# Define specific agent roles
class UrbanPlanner(Agent):
    def plan_city_layout(self):
        layout = random.choice(["Grid", "Circular", "Organic"])
        self.communicate(f"Proposed city layout: {layout}")
        return layout

class ResourceManager(Agent):
    def allocate_resources(self):
        resources = random.randint(50, 100)
        self.communicate(f"Allocated resources: {resources}")
        return resources

class ConstructionSupervisor(Agent):
    def construct_building(self, building_type):
        self.communicate(f"Started construction of: {building_type}")
        time.sleep(1)  # Simulate time taken for construction
        self.communicate(f"Completed construction of: {building_type}")

class PublicServiceCoordinator(Agent):
    def manage_services(self):
        services = ["Healthcare", "Education", "Transportation"]
        self.communicate(f"Managed services: {', '.join(services)}")

# Define the city simulation environment
class CitySimulation:
    def __init__(self):
        self.agents = [
            UrbanPlanner("Urban Planner"),
            ResourceManager("Resource Manager"),
            ConstructionSupervisor("Construction Supervisor"),
            PublicServiceCoordinator("Public Service Coordinator")
        ]

    def run_simulation(self):
        # Each agent performs their role in the simulationdef run_simulation(self):
        # Each agent shares their plans and resources
        layout = self.agents[0].plan_city_layout()
        resources = self.agents[1].allocate_resources()
        self.agents[0].communicate(f"City layout decided: {layout}")        if resources > 0:
            self.agents[2].construct_building("Residential Building")
        else:
            self.agents[0].communicate("Insufficient resources for construction.")

        # Simulate unexpected events
        if random.random() < 0.1:  # 10% chance of a disaster
            self.simulate_natural_disaster()
        self.agents[3].manage_services()        # Simulate the effects of decisions over time
        self.simulate_city_effects(layout, resources)        # Simulate the effects of decisions over time
        self.simulate_city_effects(layout, resources)

    def simulate_city_effects(self, layout, resources):
        print(f"Simulating city effects with layout: {layout} and resources: {resources}")
        # Here we can add more complex logic to simulate city dynamics
    def simulate_natural_disaster(self):
        self.communicate("A natural disaster has occurred! Resources will be affected.")
        # Logic to reduce resources or impact construction timelines

# Define test cases
def test_communication():
    urban_planner = UrbanPlanner("Test Urban Planner")
    resource_manager = ResourceManager("Test Resource Manager")
    urban_planner.communicate("Testing communication.")
    resource_manager.communicate("Communication successful.")

def test_resource_allocation():
    resource_manager = ResourceManager("Test Resource Manager")
    allocated = resource_manager.allocate_resources()
    assert allocated > 0, "Resource allocation failed."

def test_construction():
    supervisor = ConstructionSupervisor("Test Supervisor")
    supervisor.construct_building("Commercial Building")

def test_service_management():
    coordinator = PublicServiceCoordinator("Test Coordinator")
    coordinator.manage_services()

# Main execution
if __name__ == "__main__":
    # Run the city simulation
    city_simulation = CitySimulation()
    city_simulation.run_simulation()

    # Run tests
    test_communication()
    test_resource_allocation()
    test_construction()
    test_service_management()