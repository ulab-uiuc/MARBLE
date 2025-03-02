# solution.py
# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import distance

# Define a class for celestial bodies
class CelestialBody:
    def __init__(self, mass, radius, position, velocity):
        """
        Initialize a celestial body with mass, radius, position, and velocity.

        Args:
            mass (float): Mass of the celestial body.
            radius (float): Radius of the celestial body.
            position (list): Initial position of the celestial body in 3D space.
            velocity (list): Initial velocity of the celestial body in 3D space.
        """
        self.mass = mass
        self.radius = radius
        self.position = np.array(position)
        self.velocity = np.array(velocity)

# Define a class for the simulation engine
class SimulationEngine:
    def __init__(self, celestial_bodies):
        """
        Initialize the simulation engine with a list of celestial bodies.

        Args:
            celestial_bodies (list): List of CelestialBody objects.
        """
        self.celestial_bodies = celestial_bodies

    def calculate_gravitational_force(self, body1, body2):
        """
        Calculate the gravitational force between two celestial bodies.

        Args:
            body1 (CelestialBody): First celestial body.
            body2 (CelestialBody): Second celestial body.

        Returns:
            list: Gravitational force vector.
        """
        G = 6.67430e-11  # Gravitational constant
        r = body2.position - body1.position
        force = G * body1.mass * body2.mass * r / np.linalg.norm(r)**3
        return force

    def update_positions(self, dt):
        """
        Update the positions of all celestial bodies based on their velocities and the gravitational forces between them.

        Args:
            dt (float): Time step.
        """
        for i in range(len(self.celestial_bodies)):
            for j in range(i+1, len(self.celestial_bodies)):
                force = self.calculate_gravitational_force(self.celestial_bodies[i], self.celestial_bodies[j])
                self.celestial_bodies[i].velocity += force / self.celestial_bodies[i].mass * dt
                self.celestial_bodies[j].velocity -= force / self.celestial_bodies[j].mass * dt
            self.celestial_bodies[i].position += self.celestial_bodies[i].velocity * dt

# Define a class for the visualization component
class VisualizationComponent:
    def __init__(self, simulation_engine):
        """
        Initialize the visualization component with a simulation engine.

        Args:
            simulation_engine (SimulationEngine): Simulation engine.
        """
        self.simulation_engine = simulation_engine

    def plot_simulation(self, dt, t_max):
        """
        Plot the simulation results over time.

        Args:
            dt (float): Time step.
            t_max (float): Maximum time.
        """
        t = 0
        while t < t_max:
            self.simulation_engine.update_positions(dt)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            for body in self.simulation_engine.celestial_bodies:
                ax.plot(body.position[0], body.position[1], body.position[2], 'o')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show()
            t += dt

# Define a class for the educational content module
class EducationalContentModule:
    def __init__(self, visualization_component):
        """
        Initialize the educational content module with a visualization component.

        Args:
            visualization_component (VisualizationComponent): Visualization component.
        """
        self.visualization_component = visualization_component

    def display_educational_content(self):
        """
        Display educational content related to the astronomical phenomena being simulated.
        """
        print("Welcome to the educational content module!")
        print("This module provides background information, explanations, and interactive quizzes related to the astronomical phenomena being simulated.")
        print("Please select a topic to learn more:")
        print("1. Planetary Orbits")
        print("2. Stellar Evolution")
        print("3. Galactic Dynamics")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Planetary orbits are the paths that planets follow as they move around their stars.")
            print("The shape of a planetary orbit depends on the mass of the star and the planet.")
        elif choice == "2":
            print("Stellar evolution is the process by which stars change over time.")
            print("Stars are born from giant molecular clouds and eventually die in a supernova explosion.")
        elif choice == "3":
            print("Galactic dynamics is the study of the motion of galaxies and their components.")
            print("Galaxies are held together by gravity and rotate around their centers.")
        else:
            print("Invalid choice. Please try again.")

# Main function
def main():
    # Create celestial bodies
    sun = CelestialBody(1.989e30, 6.96e8, [0, 0, 0], [0, 0, 0])
    earth = CelestialBody(5.972e24, 6.371e6, [1.496e11, 0, 0], [0, 29.78e3, 0])

    # Create simulation engine
    simulation_engine = SimulationEngine([sun, earth])

    # Create visualization component
    visualization_component = VisualizationComponent(simulation_engine)

    # Create educational content module
    educational_content_module = EducationalContentModule(visualization_component)

    # Run simulation
    dt = 1e3  # Time step
    t_max = 1e7  # Maximum time
    visualization_component.plot_simulation(dt, t_max)

    # Display educational content
    educational_content_module.display_educational_content()

# Run main function
if __name__ == "__main__":
    main()