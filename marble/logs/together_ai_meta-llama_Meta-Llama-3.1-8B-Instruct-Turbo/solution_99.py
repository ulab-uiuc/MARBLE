# video_collab_editor.py
# This is the main implementation of the VideoCollabEditor system.

import threading
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List

# Define an Enum for user roles
class UserRole(Enum):
    EDITOR = 1
    REVIEWER = 2
    OWNER = 3

# Define a base class for users
class User(ABC):
    def __init__(self, name: str, role: UserRole):
        self.name = name
        self.role = role
        self.history = []

    @abstractmethod
    def edit_video(self, video: 'Video', start_time: float, end_time: float):
        pass

    @abstractmethod
    def suggest_change(self, video: 'Video', start_time: float, end_time: float, comment: str):
        pass

# Define a class for users with specific roles
class Editor(User):
    def edit_video(self, video: 'Video', start_time: float, end_time: float):
        # Implement video editing logic here
        print(f"{self.name} edited the video from {start_time} to {end_time}")
        self.history.append((start_time, end_time))

    def suggest_change(self, video: 'Video', start_time: float, end_time: float, comment: str):
        # Implement suggestion logic here
        print(f"{self.name} suggested a change from {start_time} to {end_time}: {comment}")

class Reviewer(User):
    def edit_video(self, video: 'Video', start_time: float, end_time: float):
        # Implement review logic here
        print(f"{self.name} reviewed the video from {start_time} to {end_time}")

    def suggest_change(self, video: 'Video', start_time: float, end_time: float, comment: str):
        # Implement suggestion logic here
        print(f"{self.name} suggested a change from {start_time} to {end_time}: {comment}")

class Owner(User):
    def edit_video(self, video: 'Video', start_time: float, end_time: float):
        # Implement owner logic here
        print(f"{self.name} edited the video from {start_time} to {end_time}")
        self.history.append((start_time, end_time))

    def suggest_change(self, video: 'Video', start_time: float, end_time: float, comment: str):
        # Implement suggestion logic here
        print(f"{self.name} suggested a change from {start_time} to {end_time}: {comment}")

# Define a class for videos
class Video:
    def __init__(self, name: str, duration: float):
        self.name = name
        self.duration = duration
        self.sections = []

    def add_section(self, start_time: float, end_time: float, user: User):
        self.sections.append((start_time, end_time, user))

    def get_section(self, start_time: float, end_time: float):
        for section in self.sections:
            if start_time <= section[0] and end_time >= section[1]:
                return section
        return None

# Define a class for the VideoCollabEditor system
class VideoCollabEditor:
    def __init__(self):
        self.users = {}
        self.videos = {}

    def add_user(self, user: User):
        self.users[user.name] = user

    def add_video(self, video: Video):
        self.videos[video.name] = video

    def edit_video(self, video_name: str, user_name: str, start_time: float, end_time: float):
        video = self.videos[video_name]
        user = self.users[user_name]
        user.edit_video(video, start_time, end_time)

    def suggest_change(self, video_name: str, user_name: str, start_time: float, end_time: float, comment: str):
        video = self.videos[video_name]
        user = self.users[user_name]
        user.suggest_change(video, start_time, end_time, comment)

    def get_video_history(self, video_name: str):
        video = self.videos[video_name]
        return video.sections

# Create a VideoCollabEditor instance
editor = VideoCollabEditor()

# Add users
editor.add_user(Editor("John", UserRole.EDITOR))
editor.add_user(Reviewer("Jane", UserRole.REVIEWER))
editor.add_user(Owner("Bob", UserRole.OWNER))

# Add a video
video = Video("Movie", 120.0)
editor.add_video(video)

# Edit the video
editor.edit_video("Movie", "John", 10.0, 20.0)

# Suggest a change
editor.suggest_change("Movie", "Jane", 15.0, 25.0, "This is a great scene!")

# Get the video history
history = editor.get_video_history("Movie")
for section in history:
    print(f"Section: {section[0]} to {section[1]}, User: {section[2].name}")