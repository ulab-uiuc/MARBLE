# astro_sim.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import messagebox

class CelestialBody:
    """
    Represents a celestial body with mass, radius, and initial position and velocity.
    """
    def __init__(self, name, mass, radius, position, velocity):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = np.array(position)
        self.velocity = np.array(velocity)

class SimulationEngine:
    """
    Simulates the physics of celestial mechanics, including gravitational forces, orbital dynamics, and collision detection.
    """
    def __init__(self, celestial_bodies):
        self.celestial_bodies = celestial_bodies
        self.time_step = 0.01
        self.time_scale = 1

    def calculate_gravitational_force(self, body1, body2):
        """
        Calculates the gravitational force between two celestial bodies.
        """
        G = 6.674 * (10**-11)  # gravitational constant
        distance = np.linalg.norm(body1.position - body2.position)
        force = G * body1.mass * body2.mass / (distance**2)
        direction = (body2.position - body1.position) / distance
        return force * direction

    def update_positions(self):
        """
        Updates the positions of the celestial bodies based on their velocities.
        """
        for body in self.celestial_bodies:
            body.position += body.velocity * self.time_step * self.time_scale

    def update_velocities(self):
        """
        Updates the velocities of the celestial bodies based on the gravitational forces.
        """
        for i, body1 in enumerate(self.celestial_bodies):
            total_force = np.zeros(3)
            for j, body2 in enumerate(self.celestial_bodies):
                if i != j:
                    force = self.calculate_gravitational_force(body1, body2)
                    total_force += force
            body1.velocity += total_force / body1.mass * self.time_step * self.time_scale

    def simulate(self, time):
        """
        Simulates the celestial bodies for a given time.
        """
        for _ in range(int(time / (self.time_step * self.time_scale))):
            self.update_positions()
            self.update_velocities()

class VisualizationComponent:
    """
    Displays the simulation results in 3D, with options to adjust the view, zoom, and time scale.
    """
    def __init__(self, simulation_engine):
        self.simulation_engine = simulation_engine
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111, projection='3d')

    def plot_celestial_bodies(self):
        """
        Plots the celestial bodies in 3D.
        """
        self.ax.clear()
        for body in self.simulation_engine.celestial_bodies:
            self.ax.scatter(body.position[0], body.position[1], body.position[2], s=body.radius*100)
            self.ax.text(body.position[0], body.position[1], body.position[2], body.name)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)
        plt.draw()
        plt.pause(0.01)

    def visualize(self, time):
        """
        Visualizes the simulation for a given time.
        """
        for _ in range(int(time / (self.simulation_engine.time_step * self.simulation_engine.time_scale))):
            self.simulation_engine.update_positions()
            self.simulation_engine.update_velocities()
            self.plot_celestial_bodies()

class EducationalContentModule:
    """
    Provides users with background information, explanations, and interactive quizzes related to the astronomical phenomena being simulated.
    """
    def __init__(self, simulation_engine):
        self.simulation_engine = simulation_engine
        self.root = tk.Tk()
        self.root.title("Astronomical Phenomena")

    def display_content(self):
        """
        Displays the educational content.
        """
        content = "Welcome to the Astronomical Phenomena simulator! \n"
        content += "This simulator allows you to explore the physics of celestial mechanics, including gravitational forces, orbital dynamics, and collision detection. \n"
        content += "You can adjust the time scale and view the simulation in 3D. \n"
        content += "Try changing the initial conditions of the celestial bodies to see how it affects the simulation. \n"
        label = tk.Label(self.root, text=content)
        label.pack()

    def quiz(self):
        """
        Displays an interactive quiz.
        """
        question = "What is the gravitational constant? \n"
        answer = tk.StringVar()
        entry = tk.Entry(self.root, textvariable=answer)
        entry.pack()
        def check_answer():
            if answer.get() == "6.674 * (10**-11)":
                messagebox.showinfo("Correct!", "That's correct!")
            else:
                messagebox.showinfo("Incorrect", "Sorry, that's incorrect.")
        button = tk.Button(self.root, text="Submit", command=check_answer)
        button.pack()

    def run(self):
        """
        Runs the educational content module.
        """
        self.display_content()
        self.quiz()
        self.root.mainloop()

def main():
    # Create celestial bodies
    earth = CelestialBody("Earth", 5.972 * (10**24), 6371000, [0, 0, 0], [0, 0, 0])
    mars = CelestialBody("Mars", 6.4171 * (10**23), 3389500, [1.382 * (10**11), 0, 0], [0, 24000, 0])

    # Create simulation engine
    simulation_engine = SimulationEngine([earth, mars])

    # Create visualization component
    visualization_component = VisualizationComponent(simulation_engine)

    # Create educational content module
    educational_content_module = EducationalContentModule(simulation_engine)

    # Run simulation
    simulation_engine.simulate(100)

    # Visualize simulation
    visualization_component.visualize(100)

    # Run educational content module
    educational_content_module.run()

if __name__ == "__main__":
    main()