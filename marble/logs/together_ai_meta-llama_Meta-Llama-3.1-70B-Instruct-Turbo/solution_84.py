# database.py
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_name):def create_tables(self):
    try:        # Create athlete table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS athletes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Create workout plan table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS workout_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                athlete_id INTEGER NOT NULL,
                FOREIGN KEY (athlete_id) REFERENCES athletes (id)
            )
        ''')

        # Create game strategy table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS game_strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                athlete_id INTEGER NOT NULL,
                FOREIGN KEY (athlete_id) REFERENCES athletes (id)
            )
        ''')

        # Create performance metrics table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                athlete_id INTEGER NOT NULL,
                FOREIGN KEY (athlete_id) REFERENCES athletes (id)
            )
        ''')
        self.conn.commit()
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                athlete_id INTEGER NOT NULL,
                FOREIGN KEY (athlete_id) REFERENCES athletes (id)
            )
        ''')

    def insert_athlete(self, name, email, role):
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        self.conn.execute('INSERT INTO athletes (name, email, role) VALUES (?, ?, ?)', (name, email, role))
        self.conn.commit()

    def insert_workout_plan(self, name, description, athlete_id):
        self.conn.execute('INSERT INTO workout_plans (name, description, athlete_id) VALUES (?, ?, ?)', (name, description, athlete_id))
        self.conn.commit()

    def insert_game_strategy(self, name, description, athlete_id):
        self.conn.execute('INSERT INTO game_strategies (name, description, athlete_id) VALUES (?, ?, ?)', (name, description, athlete_id))
        self.conn.commit()

    def insert_performance_metric(self, metric_name, value, athlete_id):
        self.conn.execute('INSERT INTO performance_metrics (metric_name, value, athlete_id) VALUES (?, ?, ?)', (metric_name, value, athlete_id))
        self.conn.commit()

    def get_athlete(self, id):
        cursor = self.conn.execute('SELECT * FROM athletes WHERE id = ?', (id,))
        return cursor.fetchone()

    def get_workout_plan(self, id):
        cursor = self.conn.execute('SELECT * FROM workout_plans WHERE id = ?', (id,))
        return cursor.fetchone()

    def get_game_strategy(self, id):
        cursor = self.conn.execute('SELECT * FROM game_strategies WHERE id = ?', (id,))
        return cursor.fetchone()

    def get_performance_metric(self, id):
        cursor = self.conn.execute('SELECT * FROM performance_metrics WHERE id = ?', (id,))
        return cursor.fetchone()


# backend.py
from database import Database

class Backend:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def create_athlete(self, name, email, role):
        self.db.insert_athlete(name, email, role)

    def create_workout_plan(self, name, description, athlete_id):
        self.db.insert_workout_plan(name, description, athlete_id)

    def create_game_strategy(self, name, description, athlete_id):
        self.db.insert_game_strategy(name, description, athlete_id)

    def create_performance_metric(self, metric_name, value, athlete_id):
        self.db.insert_performance_metric(metric_name, value, athlete_id)

    def get_athlete(self, id):
        return self.db.get_athlete(id)

    def get_workout_plan(self, id):
        return self.db.get_workout_plan(id)

    def get_game_strategy(self, id):
        return self.db.get_game_strategy(id)

    def get_performance_metric(self, id):
        return self.db.get_performance_metric(id)


# frontend.py
from backend import Backend

class Frontend:
    def __init__(self, backend):
        self.backend = backend

    def create_athlete(self):
        name = input("Enter athlete's name: ")
        email = input("Enter athlete's email: ")
        role = input("Enter athlete's role: ")
        self.backend.create_athlete(name, email, role)

    def create_workout_plan(self):
        name = input("Enter workout plan's name: ")
        description = input("Enter workout plan's description: ")
        athlete_id = int(input("Enter athlete's id: "))
        self.backend.create_workout_plan(name, description, athlete_id)

    def create_game_strategy(self):
        name = input("Enter game strategy's name: ")
        description = input("Enter game strategy's description: ")
        athlete_id = int(input("Enter athlete's id: "))
        self.backend.create_game_strategy(name, description, athlete_id)

    def create_performance_metric(self):
        metric_name = input("Enter performance metric's name: ")
        value = float(input("Enter performance metric's value: "))
        athlete_id = int(input("Enter athlete's id: "))
        self.backend.create_performance_metric(metric_name, value, athlete_id)

    def get_athlete(self):
        id = int(input("Enter athlete's id: "))
        athlete = self.backend.get_athlete(id)
        if athlete:
            print("Athlete's name: ", athlete[1])
            print("Athlete's email: ", athlete[2])
            print("Athlete's role: ", athlete[3])
        else:
            print("Athlete not found")

    def get_workout_plan(self):
        id = int(input("Enter workout plan's id: "))
        workout_plan = self.backend.get_workout_plan(id)
        if workout_plan:
            print("Workout plan's name: ", workout_plan[1])
            print("Workout plan's description: ", workout_plan[2])
            print("Athlete's id: ", workout_plan[3])
        else:
            print("Workout plan not found")

    def get_game_strategy(self):
        id = int(input("Enter game strategy's id: "))
        game_strategy = self.backend.get_game_strategy(id)
        if game_strategy:
            print("Game strategy's name: ", game_strategy[1])
            print("Game strategy's description: ", game_strategy[2])
            print("Athlete's id: ", game_strategy[3])
        else:
            print("Game strategy not found")

    def get_performance_metric(self):
        id = int(input("Enter performance metric's id: "))
        performance_metric = self.backend.get_performance_metric(id)
        if performance_metric:
            print("Performance metric's name: ", performance_metric[1])
            print("Performance metric's value: ", performance_metric[2])
            print("Athlete's id: ", performance_metric[3])
        else:
            print("Performance metric not found")


# solution.py
from frontend import Frontend
from backend import Backend
from database import Database

def main():
    db_name = "sport_team_coordinator.db"
    db = Database(db_name)
    db.create_tables()
    backend = Backend(db_name)
    frontend = Frontend(backend)

    while True:
        print("1. Create athlete")
        print("2. Create workout plan")
        print("3. Create game strategy")
        print("4. Create performance metric")
        print("5. Get athlete")
        print("6. Get workout plan")
        print("7. Get game strategy")
        print("8. Get performance metric")
        print("9. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            frontend.create_athlete()
        elif choice == 2:
            frontend.create_workout_plan()
        elif choice == 3:
            frontend.create_game_strategy()
        elif choice == 4:
            frontend.create_performance_metric()
        elif choice == 5:
            frontend.get_athlete()
        elif choice == 6:
            frontend.get_workout_plan()
        elif choice == 7:
            frontend.get_game_strategy()
        elif choice == 8:
            frontend.get_performance_metric()
        elif choice == 9:
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()