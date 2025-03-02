try:
    db = Database('sport_team_coordinator.db')
    db.create_tables()
except sqlite3.Error as e:
    return jsonify({'error': 'Failed to connect to database: ' + str(e)}), 500# API endpoint to create a new athlete
@app.route('/athletes', methods=['POST'])
def create_athlete():def create_athlete():
    try:
        data = request.get_json()
        db.insert_athlete(data['name'], data['email'], data['role'])
        return jsonify({'message': 'Athlete created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500@app.route('/workout-plans', methods=['POST'])
def create_workout_plan():def create_workout_plan():
    try:
        data = request.get_json()
        db.insert_workout_plan(data['athlete_id'], data['plan_name'], data['plan_description'])
        return jsonify({'message': 'Workout plan created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500@app.route('/game-strategies', methods=['POST'])
def create_game_strategy():def create_game_strategy():
    try:
        data = request.get_json()
        db.insert_game_strategy(data['athlete_id'], data['strategy_name'], data['strategy_description'])
        return jsonify({'message': 'Game strategy created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500@app.route('/performance-metrics', methods=['POST'])
def create_performance_metric():def create_performance_metric():
    try:
        data = request.get_json()
        db.insert_performance_metric(data['athlete_id'], data['metric_name'], data['metric_value'])
        return jsonify({'message': 'Performance metric created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500if __name__ == '__main__':
    app.run(debug=True)


# frontend.py
import tkinter as tk
from tkinter import ttk
from backend import app

class SportTeamCoordinator:
    def __init__(self, root):
        self.root = root
        self.root.title('Sport Team Coordinator')
        self.root.geometry('800x600')

        # Create tabs
        self.tab_control = ttk.Notebook(self.root)
        self.athlete_tab = ttk.Frame(self.tab_control)
        self.workout_plan_tab = ttk.Frame(self.tab_control)
        self.game_strategy_tab = ttk.Frame(self.tab_control)
        self.performance_metric_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.athlete_tab, text='Athletes')
        self.tab_control.add(self.workout_plan_tab, text='Workout Plans')
        self.tab_control.add(self.game_strategy_tab, text='Game Strategies')
        self.tab_control.add(self.performance_metric_tab, text='Performance Metrics')

        self.tab_control.pack(expand=1, fill='both')

        # Create athlete tab widgets
        self.athlete_name_label = tk.Label(self.athlete_tab, text='Name:')
        self.athlete_name_label.pack()
        self.athlete_name_entry = tk.Entry(self.athlete_tab)
        self.athlete_name_entry.pack()

        self.athlete_email_label = tk.Label(self.athlete_tab, text='Email:')
        self.athlete_email_label.pack()
        self.athlete_email_entry = tk.Entry(self.athlete_tab)
        self.athlete_email_entry.pack()

        self.athlete_role_label = tk.Label(self.athlete_tab, text='Role:')
        self.athlete_role_label.pack()
        self.athlete_role_entry = tk.Entry(self.athlete_tab)
        self.athlete_role_entry.pack()

        self.create_athlete_button = tk.Button(self.athlete_tab, text='Create Athlete', command=self.create_athlete)
        self.create_athlete_button.pack()

        # Create workout plan tab widgets
        self.workout_plan_athlete_id_label = tk.Label(self.workout_plan_tab, text='Athlete ID:')
        self.workout_plan_athlete_id_label.pack()
        self.workout_plan_athlete_id_entry = tk.Entry(self.workout_plan_tab)
        self.workout_plan_athlete_id_entry.pack()

        self.workout_plan_name_label = tk.Label(self.workout_plan_tab, text='Plan Name:')
        self.workout_plan_name_label.pack()
        self.workout_plan_name_entry = tk.Entry(self.workout_plan_tab)
        self.workout_plan_name_entry.pack()

        self.workout_plan_description_label = tk.Label(self.workout_plan_tab, text='Plan Description:')
        self.workout_plan_description_label.pack()
        self.workout_plan_description_entry = tk.Entry(self.workout_plan_tab)
        self.workout_plan_description_entry.pack()

        self.create_workout_plan_button = tk.Button(self.workout_plan_tab, text='Create Workout Plan', command=self.create_workout_plan)
        self.create_workout_plan_button.pack()

        # Create game strategy tab widgets
        self.game_strategy_athlete_id_label = tk.Label(self.game_strategy_tab, text='Athlete ID:')
        self.game_strategy_athlete_id_label.pack()
        self.game_strategy_athlete_id_entry = tk.Entry(self.game_strategy_tab)
        self.game_strategy_athlete_id_entry.pack()

        self.game_strategy_name_label = tk.Label(self.game_strategy_tab, text='Strategy Name:')
        self.game_strategy_name_label.pack()
        self.game_strategy_name_entry = tk.Entry(self.game_strategy_tab)
        self.game_strategy_name_entry.pack()

        self.game_strategy_description_label = tk.Label(self.game_strategy_tab, text='Strategy Description:')
        self.game_strategy_description_label.pack()
        self.game_strategy_description_entry = tk.Entry(self.game_strategy_tab)
        self.game_strategy_description_entry.pack()

        self.create_game_strategy_button = tk.Button(self.game_strategy_tab, text='Create Game Strategy', command=self.create_game_strategy)
        self.create_game_strategy_button.pack()

        # Create performance metric tab widgets
        self.performance_metric_athlete_id_label = tk.Label(self.performance_metric_tab, text='Athlete ID:')
        self.performance_metric_athlete_id_label.pack()
        self.performance_metric_athlete_id_entry = tk.Entry(self.performance_metric_tab)
        self.performance_metric_athlete_id_entry.pack()

        self.performance_metric_name_label = tk.Label(self.performance_metric_tab, text='Metric Name:')
        self.performance_metric_name_label.pack()
        self.performance_metric_name_entry = tk.Entry(self.performance_metric_tab)
        self.performance_metric_name_entry.pack()

        self.performance_metric_value_label = tk.Label(self.performance_metric_tab, text='Metric Value:')
        self.performance_metric_value_label.pack()
        self.performance_metric_value_entry = tk.Entry(self.performance_metric_tab)
        self.performance_metric_value_entry.pack()

        self.create_performance_metric_button = tk.Button(self.performance_metric_tab, text='Create Performance Metric', command=self.create_performance_metric)
        self.create_performance_metric_button.pack()

    def create_athlete(self):
        name = self.athlete_name_entry.get()
        email = self.athlete_email_entry.get()
        role = self.athlete_role_entry.get()

        import requests
        response = requests.post('http://localhost:5000/athletes', json={'name': name, 'email': email, 'role': role})
        print(response.text)

    def create_workout_plan(self):
        athlete_id = self.workout_plan_athlete_id_entry.get()
        plan_name = self.workout_plan_name_entry.get()
        plan_description = self.workout_plan_description_entry.get()

        import requests
        response = requests.post('http://localhost:5000/workout-plans', json={'athlete_id': athlete_id, 'plan_name': plan_name, 'plan_description': plan_description})
        print(response.text)

    def create_game_strategy(self):
        athlete_id = self.game_strategy_athlete_id_entry.get()
        strategy_name = self.game_strategy_name_entry.get()
        strategy_description = self.game_strategy_description_entry.get()

        import requests
        response = requests.post('http://localhost:5000/game-strategies', json={'athlete_id': athlete_id, 'strategy_name': strategy_name, 'strategy_description': strategy_description})
        print(response.text)

    def create_performance_metric(self):
        athlete_id = self.performance_metric_athlete_id_entry.get()
        metric_name = self.performance_metric_name_entry.get()
        metric_value = self.performance_metric_value_entry.get()

        import requests
        response = requests.post('http://localhost:5000/performance-metrics', json={'athlete_id': athlete_id, 'metric_name': metric_name, 'metric_value': metric_value})
        print(response.text)

if __name__ == '__main__':
    root = tk.Tk()
    app = SportTeamCoordinator(root)
    root.mainloop()