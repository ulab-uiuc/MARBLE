# drift_collaboration.py
# This is the main implementation of the Drift_Collaboration game.

import pygame
import random
import threading
import socket
import json

# Initialize Pygame
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set the width and height of the screen (width, height).
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Drift Collaboration")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.x = random.randint(0, size[0])
        self.y = random.randint(0, size[1])
        self.speed = 5
        self.drift_angle = 0
        self.drift_duration = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

class Drift_Collaboration:
    def __init__(self):
        self.players = []
        self.server_socket = None
        self.client_sockets = []
        self.chat_log = []

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)
        print("Server started. Waiting for connections...")

    def start_client(self, name):
        self.client_sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.client_sockets[-1].connect(('localhost', 12345))
        self.client_sockets[-1].sendall(name.encode())

    def handle_client(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"New connection from {address}")
            client_socket.sendall("Welcome to Drift Collaboration!".encode())

    def send_message(self, message):
        for client_socket in self.client_sockets:
            client_socket.sendall(message.encode())

    def receive_message(self):
        for client_socket in self.client_sockets:
            message = client_socket.recv(1024).decode()
            if message:
                self.chat_log.append(message)
                print(message)

    def update(self):
        for player in self.players:
            player.move()
            self.send_message(f"{player.name} is at ({player.x}, {player.y})")

    def draw(self):
        screen.fill(WHITE)
        for player in self.players:
            pygame.draw.rect(screen, player.color, (player.x, player.y, 50, 50))
        for message in self.chat_log:
            font = pygame.font.Font(None, 24)
            text = font.render(message, True, (0, 0, 0))
            screen.blit(text, (10, 10))
            self.chat_log.remove(message)
        pygame.display.flip()

def main():
    game = Drift_Collaboration()
    game.start_server()
    threading.Thread(target=game.handle_client).start()

    player1 = Player("Player 1", RED)
    player2 = Player("Player 2", GREEN)
    game.players.append(player1)
    game.players.append(player2)

    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.send_message("Drift!")
                    player1.drift_angle = random.randint(-30, 30)
                    player2.drift_angle = random.randint(-30, 30)
                    player1.drift_duration = random.randint(1, 10)
                    player2.drift_duration = random.randint(1, 10)
                    game.send_message(f"{player1.name} is drifting for {player1.drift_duration} seconds at an angle of {player1.drift_angle} degrees")
                    game.send_message(f"{player2.name} is drifting for {player2.drift_duration} seconds at an angle of {player2.drift_angle} degrees")

        game.update()
        game.draw()
        game.receive_message()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()