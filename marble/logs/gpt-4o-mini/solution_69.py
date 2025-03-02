# solution.py

# This module defines the parameters for celestial bodies
class CelestialBody:
    def __init__(self, name, mass, radius, position, velocity):
        """
        Initializes a celestial body with the given parameters.

        :param name: Name of the celestial body
        :param mass: Mass of the celestial body (in kg)
        :param radius: Radius of the celestial body (in meters)
        :param position: Initial position (x, y, z) in meters
        :param velocity: Initial velocity (vx, vy, vz) in meters/second
        """
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = position  # Tuple (x, y, z)
        self.velocity = velocity  # Tuple (vx, vy, vz)

# This module handles the simulation of celestial mechanics
class SimulationEngine:
    G = 6.67430e-11  # Gravitational constant

    def __init__(self):
        self.bodies = []

    def add_body(self, body):
        """
        Adds a celestial body to the simulation.

        :param body: An instance of CelestialBody
        """
        self.bodies.append(body)

    def compute_gravitational_force(self, body1, body2):
        """
        Computes the gravitational force between two celestial bodies.

        :param body1: First celestial body
        :param body2: Second celestial body
        :return: Gravitational force vector (fx, fy, fz)
        """
        # Calculate the distance vector
        dx = body2.position[0] - body1.position[0]
        dy = body2.position[1] - body1.position[1]
        dz = body2.position[2] - body1.position[2]
        distance = (dx**2 + dy**2 + dz**2)**0.5

        # Calculate the gravitational force magnitude        if distance == 0:
            return (0, 0, 0)
        else:
            force_magnitude = self.G * (body1.mass * body2.mass) / distance**2        # Calculate the force vector
        fx = force_magnitude * (dx / distance)
        fy = force_magnitude * (dy / distance)
        fz = force_magnitude * (dz / distance)

        return (fx, fy, fz)

    def update_positions(self, time_step):
        """
        Updates the positions of all celestial bodies based on their velocities.

        :param time_step: Time step for the simulation (in seconds)
        """
        for body in self.bodies:
            # Update position based on current velocity
            body.position = (
                body.position[0] + body.velocity[0] * time_step,
                body.position[1] + body.velocity[1] * time_step,
                body.position[2] + body.velocity[2] * time_step
            )

    def simulate(self, time_step, duration):
        """
        Runs the simulation for a specified duration.

        :param time_step: Time step for the simulation (in seconds)
        :param duration: Total duration of the simulation (in seconds)
        """
        steps = int(duration / time_step)
        for _ in range(steps):
            # Calculate forces and update velocities
            for i in range(len(self.bodies)):
                total_force = (0, 0, 0)
                for j in range(len(self.bodies)):
                    if i != j:
                        force = self.compute_gravitational_force(self.bodies[i], self.bodies[j])
                        total_force = (total_force[0] + force[0],
                                       total_force[1] + force[1],
                                       total_force[2] + force[2])
                
                # Update velocity based on total force
                ax = total_force[0] / self.bodies[i].mass
                ay = total_force[1] / self.bodies[i].mass
                az = total_force[2] / self.bodies[i].mass
                self.bodies[i].velocity = (
                    self.bodies[i].velocity[0] + ax * time_step,
                    self.bodies[i].velocity[1] + ay * time_step,
                    self.bodies[i].velocity[2] + az * time_step
                )
            
            # Update positions after velocities are updated
            self.update_positions(time_step)

# This module handles the visualization of the simulation
class Visualization:
    def __init__(self, simulation_engine):
        """
        Initializes the visualization component.

        :param simulation_engine: An instance of SimulationEngine
        """
        self.simulation_engine = simulation_engine

    def display(self):
        """
        Displays the current state of the simulation in a 3D space.
        This is a placeholder for actual visualization code.
        """
        for body in self.simulation_engine.bodies:
            print(f"{body.name}: Position = {body.position}, Velocity = {body.velocity}")

# This module provides educational content related to the simulation
class EducationalContent:
    def __init__(self):
        """
        Initializes the educational content module.
        """
        self.content = {
            "gravity": "Gravity is a force that attracts two bodies towards each other.",
            "orbits": "Orbits are the paths that celestial bodies follow around a star or planet."
        }

    def get_content(self, topic):
        """
        Retrieves educational content for a given topic.

        :param topic: The topic for which to retrieve content
        :return: Educational content as a string
        """
        return self.content.get(topic, "Content not found.")

# Main execution of the AstroSim application
if __name__ == "__main__":
    # Create celestial bodies
    earth = CelestialBody("Earth", 5.972e24, 6.371e6, (0, 0, 0), (0, 0, 0))
    moon = CelestialBody("Moon", 7.348e22, 1.737e6, (3.844e8, 0, 0), (0, 1.022e3, 0))

    # Initialize simulation engine and add bodies
    sim_engine = SimulationEngine()
    sim_engine.add_body(earth)
    sim_engine.add_body(moon)

    # Run the simulation
    sim_engine.simulate(time_step=60, duration=3600)  # Simulate for 1 hour with 1-minute time steps

    # Initialize visualization and display results
    visualization = Visualization(sim_engine)
    visualization.display()

    # Educational content example
    edu_content = EducationalContent()
    print(edu_content.get_content("gravity"))