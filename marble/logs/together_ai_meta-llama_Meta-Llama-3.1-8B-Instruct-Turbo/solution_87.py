# user.py
class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"


# user_repository.py
class UserRepository:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_user(self, id):
        for user in self.users:
            if user.id == id:
                return user
        return None

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None


# video_analyzer.py
import cv2
import numpy as np

class VideoAnalyzer:
    def __init__(self):
        self.video_capture = None

    def analyze_video(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)
        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if not ret:
                break
            # Detect and track player movements
            # Measure key performance metrics such as speed, accuracy, and agility
            # For simplicity, we'll just display the frame
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video_capture.release()
        cv2.destroyAllWindows()

    def get_performance_metrics(self, video_path):
        # For simplicity, we'll just return some dummy metrics
        return {
            'speed': 10,
            'accuracy': 80,
            'agility': 90
        }


# performance_dashboard.py
import matplotlib.pyplot as plt

class PerformanceDashboard:
    def __init__(self):
        self.metrics = {}

    def add_metric(self, player_id, metric_name, value):
        if player_id not in self.metrics:
            self.metrics[player_id] = {}
        self.metrics[player_id][metric_name] = value

    def display_dashboard(self):
        for player_id, metrics in self.metrics.items():
            plt.bar(metrics.keys(), metrics.values())
            plt.xlabel('Metric')
            plt.ylabel('Value')
            plt.title(f'Player {player_id} Dashboard')
            plt.show()


# collaborative_workspace.py
class CollaborativeWorkspace:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def display_workspace(self):
        for message in self.messages:
            print(message)


# solution.py
from user import User
from user_repository import UserRepository
from video_analyzer import VideoAnalyzer
from performance_dashboard import PerformanceDashboard
from collaborative_workspace import CollaborativeWorkspace

class SportsTeamSyncer:
    def __init__(self):
        self.user_repository = UserRepository()
        self.video_analyzer = VideoAnalyzer()
        self.performance_dashboard = PerformanceDashboard()
        self.collaborative_workspace = CollaborativeWorkspace()

    def authenticate_user(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if user and user.password == password:
            return user
        return None

    def analyze_video(self, video_path):
        self.video_analyzer.analyze_video(video_path)

    def get_performance_metrics(self, video_path):
        return self.video_analyzer.get_performance_metrics(video_path)

    def add_metric(self, player_id, metric_name, value):
        self.performance_dashboard.add_metric(player_id, metric_name, value)

    def display_dashboard(self):
        self.performance_dashboard.display_dashboard()

    def add_message(self, message):
        self.collaborative_workspace.add_message(message)

    def display_workspace(self):
        self.collaborative_workspace.display_workspace()


# Test cases
if __name__ == '__main__':
    sports_team_syncer = SportsTeamSyncer()

    # Create users
    user_repository = UserRepository()
    user_repository.add_user(User(1, 'coach', 'password', 'coach'))
    user_repository.add_user(User(2, 'player', 'password', 'player'))
    user_repository.add_user(User(3, 'analyst', 'password', 'analyst'))

    # Authenticate user
    user = sports_team_syncer.authenticate_user('coach', 'password')
    print(user)

    # Analyze video
    sports_team_syncer.analyze_video('path/to/video.mp4')

    # Get performance metrics
    metrics = sports_team_syncer.get_performance_metrics('path/to/video.mp4')
    print(metrics)

    # Add metric
    sports_team_syncer.add_metric(1, 'speed', 10)
    sports_team_syncer.add_metric(2, 'accuracy', 80)
    sports_team_syncer.add_metric(3, 'agility', 90)

    # Display dashboard
    sports_team_syncer.display_dashboard()

    # Add message
    sports_team_syncer.add_message('Hello, team!')

    # Display workspace
    sports_team_syncer.display_workspace()