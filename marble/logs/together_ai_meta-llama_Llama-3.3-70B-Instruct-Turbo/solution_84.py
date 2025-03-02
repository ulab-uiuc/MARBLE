# database.py
import sqlite3
from sqlite3 import Error

class Database:def create_tables(self):
    try:
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS athlete_profiles (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS workout_plans (
                id INTEGER PRIMARY KEY,
                athlete_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                plan_description TEXT NOT NULL,
                FOREIGN KEY (athlete_id) REFERENCES athlete_profiles (id)
            );
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS game_strategies (
                id INTEGER PRIMARY KEY,
                team_name TEXT NOT NULL,
                strategy_name TEXT NOT NULL,
                strategy_description TEXT NOT NULL
            );
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY,
                athlete_id INTEGER NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                FOREIGN KEY (athlete_id) REFERENCES athlete_profiles (id)
            );
        ''')
    except Error as e:
        print(e)
    try:
        athlete_id = self.performance_metrics_athlete_id_entry.get()
        metric_name = self.performance_metrics_metric_name_entry.get()
        metric_value = self.performance_metrics_metric_value_entry.get()
        response = requests.post('http://localhost:5000/performance_metrics', json={'athlete_id': athlete_id, 'metric_name': metric_name, 'metric_value': metric_value})
        response.raise_for_status()
        print('Performance metric created successfully')
    except requests.exceptions.RequestException as e:
        print(f'Error creating performance metric: {e}')if __name__ == '__main__':
    root = tk.Tk()
    app = SportTeamCoordinator(root)
    root.mainloop()


# analytics.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class Analytics:
    def __init__(self, data):
        self.data = data

    def train_model(self):
        X = self.data[['athlete_id', 'metric_name']]
        y = self.data['metric_value']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

    def predict_performance(self, athlete_id, metric_name):
        X = pd.DataFrame({'athlete_id': [athlete_id], 'metric_name': [metric_name]})
        model = LinearRegression()
        model.fit(self.data[['athlete_id', 'metric_name']], self.data['metric_value'])
        y_pred = model.predict(X)
        return y_pred[0]

if __name__ == '__main__':
    data = pd.read_csv('performance_metrics.csv')
    analytics = Analytics(data)
    analytics.train_model()
    athlete_id = 1
    metric_name = 'speed'
    predicted_performance = analytics.predict_performance(athlete_id, metric_name)
    print(f'Predicted performance for athlete {athlete_id} in {metric_name}: {predicted_performance}')


# solution.py
if __name__ == '__main__':
    import database
    import backend
    import frontend
    import analytics