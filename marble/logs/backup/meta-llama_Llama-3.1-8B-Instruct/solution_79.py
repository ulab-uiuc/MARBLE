# solution.py
# Importing necessary libraries
import random
import time
import matplotlib.pyplot as plt

# Defining the Agent class
class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.resources = 100  # Initial resources for each agent

    def communicate(self, message):
        print(f"{self.name} ({self.role}) received message: {message}")

    def allocate_resources(self, amount):
        if amount <= self.resources:
            self.resources -= amount
            print(f"{self.name} ({self.role}) allocated {amount} resources")
        else:
            print(f"{self.name} ({self.role}) does not have enough resources")

    def update_status(self):
        print(f"{self.name} ({self.role}) status: resources = {self.resources}")


# Defining the UrbanPlanner class
class UrbanPlanner(Agent):
    def __init__(self, name):
        super().__init__(name, "Urban Planner")
        self.city_layout = {"blocks": 10, "roads": 20}

    def plan_city(self):
        print(f"{self.name} ({self.role}) planning city layout")
        self.city_layout["blocks"] += 5
        self.city_layout["roads"] += 10
        print(f"City layout updated: blocks = {self.city_layout['blocks']}, roads = {self.city_layout['roads']}")


# Defining the ResourceManager class
class ResourceManager(Agent):
    def __init__(self, name):
        super().__init__(name, "Resource Manager")
        self.resources_available = {"water": 100, "electricity": 100, "food": 100}

    def manage_resources(self):
        print(f"{self.name} ({self.role}) managing resources")
        self.resources_available["water"] += 20
        self.resources_available["electricity"] += 30
        self.resources_available["food"] += 40
        print(f"Resources available: water = {self.resources_available['water']}, electricity = {self.resources_available['electricity']}, food = {self.resources_available['food']}")


# Defining the ConstructionSupervisor class
class ConstructionSupervisor(Agent):
    def __init__(self, name):
        super().__init__(name, "Construction Supervisor")
        self.construction_projects = {"building": 0, "road": 0}

    def supervise_construction(self):
        print(f"{self.name} ({self.role}) supervising construction")
        self.construction_projects["building"] += 1
        self.construction_projects["road"] += 2
        print(f"Construction projects updated: building = {self.construction_projects['building']}, road = {self.construction_projects['road']}")


# Defining the PublicServiceCoordinator class
class PublicServiceCoordinator(Agent):
    def __init__(self, name):
        super().__init__(name, "Public Service Coordinator")
        self.public_services = {"police": 0, "fire": 0, "hospital": 0}

    def coordinate_public_services(self):
        print(f"{self.name} ({self.role}) coordinating public services")
        self.public_services["police"] += 1
        self.public_services["fire"] += 2
        self.public_services["hospital"] += 3
        print(f"Public services updated: police = {self.public_services['police']}, fire = {self.public_services['fire']}, hospital = {self.public_services['hospital']}")


# Defining the City class
class City:
    def __init__(self):
        self.agents = []
        self.city_layout = {"blocks": 0, "roads": 0}
        self.resources_available = {"water": 0, "electricity": 0, "food": 0}
        self.construction_projects = {"building": 0, "road": 0}
        self.public_services = {"police": 0, "fire": 0, "hospital": 0}

    def add_agent(self, agent):
        self.agents.append(agent)

    def update_status(self):
        print(f"City status: blocks = {self.city_layout['blocks']}, roads = {self.city_layout['roads']}")
        print(f"Resources available: water = {self.resources_available['water']}, electricity = {self.resources_available['electricity']}, food = {self.resources_available['food']}")
        print(f"Construction projects: building = {self.construction_projects['building']}, road = {self.construction_projects['road']}")
        print(f"Public services: police = {self.public_services['police']}, fire = {self.public_services['fire']}, hospital = {self.public_services['hospital']}")

    def simulate(self):
        for agent in self.agents:
            agent.update_status()
            if isinstance(agent, UrbanPlanner):
                agent.plan_city()
            elif isinstance(agent, ResourceManager):
                agent.manage_resources()
            elif isinstance(agent, ConstructionSupervisor):
                agent.supervise_construction()
            elif isinstance(agent, PublicServiceCoordinator):
                agent.coordinate_public_services()
        self.update_status()
        time.sleep(1)  # Pause for 1 second


# Creating agents
urban_planner = UrbanPlanner("Urban Planner 1")
resource_manager = ResourceManager("Resource Manager 1")
construction_supervisor = ConstructionSupervisor("Construction Supervisor 1")
public_service_coordinator = PublicServiceCoordinator("Public Service Coordinator 1")

# Creating city
city = City()
city.add_agent(urban_planner)
city.add_agent(resource_manager)
city.add_agent(construction_supervisor)
city.add_agent(public_service_coordinator)

# Simulating city
for i in range(10):
    city.simulate()

# Plotting city layout
plt.bar(["Blocks", "Roads"], [city.city_layout["blocks"], city.city_layout["roads"]])
plt.xlabel("City Layout")
plt.ylabel("Number of Units")
plt.title("City Layout Over Time")
plt.show()

# Plotting resources available
plt.bar(["Water", "Electricity", "Food"], [city.resources_available["water"], city.resources_available["electricity"], city.resources_available["food"]])
plt.xlabel("Resources Available")
plt.ylabel("Quantity")
plt.title("Resources Available Over Time")
plt.show()

# Plotting construction projects
plt.bar(["Building", "Road"], [city.construction_projects["building"], city.construction_projects["road"]])
plt.xlabel("Construction Projects")
plt.ylabel("Number of Units")
plt.title("Construction Projects Over Time")
plt.show()

# Plotting public services
plt.bar(["Police", "Fire", "Hospital"], [city.public_services["police"], city.public_services["fire"], city.public_services["hospital"]])
plt.xlabel("Public Services")
plt.ylabel("Number of Units")
plt.title("Public Services Over Time")
plt.show()