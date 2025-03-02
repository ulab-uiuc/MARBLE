# database.py
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_tables(self):
        # Create player profiles table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS player_profiles
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)
        ''')

        # Create team information table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS team_info
            (id INTEGER PRIMARY KEY AUTOINCREMENT, team_name TEXT, player_id INTEGER, FOREIGN KEY (player_id) REFERENCES player_profiles (id))
        ''')

        # Create game progress table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS game_progress
            (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, team_id INTEGER, progress TEXT, FOREIGN KEY (team_id) REFERENCES team_info (id))
        ''')

        # Create historical gameplay data table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS historical_gameplay_data
            (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, team_id INTEGER, outcome TEXT, FOREIGN KEY (team_id) REFERENCES team_info (id))
        ''')

    def insert_player(self, name, email):
        self.conn.execute('INSERT INTO player_profiles (name, email) VALUES (?, ?)', (name, email))
        self.conn.commit()

    def insert_team(self, team_name, player_id):
        self.conn.execute('INSERT INTO team_info (team_name, player_id) VALUES (?, ?)', (team_name, player_id))
        self.conn.commit()

    def insert_game_progress(self, game_id, team_id, progress):
        self.conn.execute('INSERT INTO game_progress (game_id, team_id, progress) VALUES (?, ?, ?)', (game_id, team_id, progress))
        self.conn.commit()

    def insert_historical_gameplay_data(self, game_id, team_id, outcome):
        self.conn.execute('INSERT INTO historical_gameplay_data (game_id, team_id, outcome) VALUES (?, ?, ?)', (game_id, team_id, outcome))
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()


# backend.py
import socket
import threading
from database import Database

class Backend:def handle_client(self, conn, addr):
    print(f'New connection from {addr}')
    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            print(f'Received message from {addr}: {message.decode()}')
            # Handle message from client
            try:
                if message.decode().startswith('join_team'):
                    team_name = message.decode().split(':')[1]
                    player_id = message.decode().split(':')[2]
                    self.db.insert_team(team_name, player_id)
                elif message.decode().startswith('update_game_progress'):
                    game_id = message.decode().split(':')[1]
                    team_id = message.decode().split(':')[2]
                    progress = message.decode().split(':')[3]
                    self.db.insert_game_progress(game_id, team_id, progress)
                elif message.decode().startswith('update_historical_gameplay_data'):
                    game_id = message.decode().split(':')[1]
                    team_id = message.decode().split(':')[2]
                    outcome = message.decode().split(':')[3]
                    self.db.insert_historical_gameplay_data(game_id, team_id, outcome)
                else:
                    print(f'Unknown message format: {message.decode()}')
            except (IndexError, ValueError) as e:
                print(f'Error parsing message: {e}')
        except:
            break

    print(f'Connection closed from {addr}')
    conn.close()print(f'New connection from {addr}')

        while True:
            try:
                message = conn.recv(1024)
                if not message:
                    break
                print(f'Received message from {addr}: {message.decode()}')
                # Handle message from client
                if message.decode().startswith('join_team'):
                    team_name = message.decode().split(':')[1]
                    player_id = message.decode().split(':')[2]
                    self.db.insert_team(team_name, player_id)
                elif message.decode().startswith('update_game_progress'):
                    game_id = message.decode().split(':')[1]
                    team_id = message.decode().split(':')[2]
                    progress = message.decode().split(':')[3]
                    self.db.insert_game_progress(game_id, team_id, progress)
                elif message.decode().startswith('update_historical_gameplay_data'):
                    game_id = message.decode().split(':')[1]
                    team_id = message.decode().split(':')[2]
                    outcome = message.decode().split(':')[3]
                    self.db.insert_historical_gameplay_data(game_id, team_id, outcome)
            except:
                break

        print(f'Connection closed from {addr}')
        conn.close()

    def start(self):
        print(f'Server started on {self.host}:{self.port}')
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()


# frontend.py
import socket
import threading
from tkinter import Tk, Label, Button, Entry, Text

class Frontend:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.root = Tk()
        self.root.title('Board Game Team Challenge')

        self.team_name_label = Label(self.root, text='Team Name:')
        self.team_name_label.pack()
        self.team_name_entry = Entry(self.root)
        self.team_name_entry.pack()

        self.player_id_label = Label(self.root, text='Player ID:')
        self.player_id_label.pack()
        self.player_id_entry = Entry(self.root)
        self.player_id_entry.pack()

        self.join_team_button = Button(self.root, text='Join Team', command=self.join_team)
        self.join_team_button.pack()

        self.game_progress_label = Label(self.root, text='Game Progress:')
        self.game_progress_label.pack()
        self.game_progress_entry = Entry(self.root)
        self.game_progress_entry.pack()

        self.update_game_progress_button = Button(self.root, text='Update Game Progress', command=self.update_game_progress)
        self.update_game_progress_button.pack()

        self.historical_gameplay_data_label = Label(self.root, text='Historical Gameplay Data:')
        self.historical_gameplay_data_label.pack()
        self.historical_gameplay_data_entry = Entry(self.root)
        self.historical_gameplay_data_entry.pack()

        self.update_historical_gameplay_data_button = Button(self.root, text='Update Historical Gameplay Data', command=self.update_historical_gameplay_data)
        self.update_historical_gameplay_data_button.pack()

        self.chat_label = Label(self.root, text='Chat:')
        self.chat_label.pack()
        self.chat_text = Text(self.root)
        self.chat_text.pack()

        self.send_message_button = Button(self.root, text='Send Message', command=self.send_message)
        self.send_message_button.pack()

        self.receive_message_thread = threading.Thread(target=self.receive_message)
        self.receive_message_thread.start()

    def join_team(self):
        team_name = self.team_name_entry.get()
        player_id = self.player_id_entry.get()
        message = f'join_team:{team_name}:{player_id}'
        self.client.send(message.encode())

    def update_game_progress(self):
        game_id = '1'  # Replace with actual game ID
        team_id = '1'  # Replace with actual team ID
        progress = self.game_progress_entry.get()
        message = f'update_game_progress:{game_id}:{team_id}:{progress}'
        self.client.send(message.encode())

    def update_historical_gameplay_data(self):
        game_id = '1'  # Replace with actual game ID
        team_id = '1'  # Replace with actual team ID
        outcome = self.historical_gameplay_data_entry.get()
        message = f'update_historical_gameplay_data:{game_id}:{team_id}:{outcome}'
        self.client.send(message.encode())

    def send_message(self):
        message = self.chat_text.get('1.0', 'end-1c')
        self.client.send(message.encode())

    def receive_message(self):
        while True:
            try:
                message = self.client.recv(1024)
                if not message:
                    break
                print(f'Received message: {message.decode()}')
                self.chat_text.insert('end', message.decode() + '\n')
            except:
                break

    def start(self):
        self.root.mainloop()


# analytics.py
import matplotlib.pyplot as plt
from database import Database

class Analytics:
    def __init__(self, db_file):
        self.db = Database(db_file)
        self.db.create_tables()

    def get_game_outcomes(self):
        cursor = self.db.conn.execute('SELECT outcome FROM historical_gameplay_data')
        outcomes = [row[0] for row in cursor.fetchall()]
        return outcomes

    def get_strategy_success_rates(self):
        cursor = self.db.conn.execute('SELECT progress FROM game_progress')
        progress = [row[0] for row in cursor.fetchall()]
        return progress

    def get_player_performance_metrics(self):
        cursor = self.db.conn.execute('SELECT name, email FROM player_profiles')
        players = [row for row in cursor.fetchall()]
        return players

    def visualize_game_outcomes(self):
        outcomes = self.get_game_outcomes()
        plt.bar(outcomes, [outcomes.count(outcome) for outcome in set(outcomes)])
        plt.xlabel('Outcome')
        plt.ylabel('Frequency')
        plt.title('Game Outcomes')
        plt.show()

    def visualize_strategy_success_rates(self):
        progress = self.get_strategy_success_rates()
        plt.bar(progress, [progress.count(p) for p in set(progress)])
        plt.xlabel('Progress')
        plt.ylabel('Frequency')
        plt.title('Strategy Success Rates')
        plt.show()

    def visualize_player_performance_metrics(self):
        players = self.get_player_performance_metrics()
        plt.bar([player[0] for player in players], [player[1] for player in players])
        plt.xlabel('Player')
        plt.ylabel('Email')
        plt.title('Player Performance Metrics')
        plt.show()


# solution.py
if __name__ == '__main__':backend = Backend('localhost', 12345, 'game_data.db')    backend_thread = threading.Thread(target=backend.start)
    backend_thread.start()

    frontend = Frontend('localhost', 12345)
    frontend.start()

    analytics = Analytics('game_data.db')
    analytics.visualize_game_outcomes()
    analytics.visualize_strategy_success_rates()
    analytics.visualize_player_performance_metrics()