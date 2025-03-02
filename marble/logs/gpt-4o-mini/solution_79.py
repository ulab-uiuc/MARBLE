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
        time_to_construct = random.randint(1, 3)
        self.communicate(f"Started constructing {building_type}. It will take {time_to_construct} hours.")
        time.sleep(time_to_construct)  # Simulate construction time
        self.communicate(f"Completed constructing {building_type}.")

class PublicServiceCoordinator(Agent):
    def ensure_wellbeing(self):
        wellbeing_status = random.choice(["Good", "Average", "Poor"])
        self.communicate(f"City wellbeing status: {wellbeing_status}")
        return wellbeing_status

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
        # Simulate the planning and construction process
        layout = self.agents[0].plan_city_layout()
        # Implement communication protocol        resources = self.agents[1].allocate_resources()
        self.agents[0].communicate(f"{self.agents[0].name} proposed layout: {layout}")
        self.agents[1].communicate(f"{self.agents[1].name} allocated resources: {resources}")        resources = self.agents[1].allocate_resources()
        self.agents[2].construct_building("Residential Building")
        self.agents[3].ensure_wellbeing()

# Define test cases
def test_communication():
    urban_planner = UrbanPlanner("Test Urban Planner")
    resource_manager = ResourceManager("Test Resource Manager")
    urban_planner.communicate("Testing communication.")
    resource_manager.communicate("Communication successful.")

def test_resource_allocation():
    resource_manager = ResourceManager("Test Resource Manager")
    allocated_resources = resource_manager.allocate_resources()
    assert allocated_resources > 0, "Resource allocation failed."

def test_construction():
    supervisor = ConstructionSupervisor("Test Supervisor")
    supervisor.construct_building("Commercial Building")

def test_wellbeing():
    coordinator = PublicServiceCoordinator("Test Coordinator")
    status = coordinator.ensure_wellbeing()
    assert status in ["Good", "Average", "Poor"], "Wellbeing status is invalid."

# Main execution
if __name__ == "__main__":
    # Run the city simulation
    city_simulation = CitySimulation()
    city_simulation.run_simulation()

    # Run tests
    test_communication()
    test_resource_allocation()
    test_construction()
    test_wellbeing()