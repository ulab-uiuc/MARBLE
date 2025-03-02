# video_collaboration_suite.py

import threading
from datetime import datetime
import time

class VideoCollaborationSuite:
    def __init__(self):
        self.video_file = None
        self.subtitle_file = None
        self.users = []
        self.chat_log = []
        self.version_control = []
        self.playback_speed = 1.0
        self.subtitle_sync_status = False

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)

    def upload_video(self, video_file):
        self.video_file = video_file

    def upload_subtitle(self, subtitle_file):
        self.subtitle_file = subtitle_file

    def sync_subtitles(self):
        # Simulate automatic subtitle synchronization
        self.subtitle_sync_status = True
        print("Subtitles synchronized.")

    def adjust_subtitle_sync(self, adjustment):
        # Simulate manual subtitle synchronization adjustment
        print(f"Subtitle synchronization adjusted by {adjustment} seconds.")

    def adjust_playback_speed(self, speed):
        self.playback_speed = speed
        print(f"Playback speed adjusted to {speed}x.")

    def send_message(self, user, message):
        self.chat_log.append((user, message, datetime.now()))
        print(f"{user}: {message}")

    def save_version(self):
        # Simulate saving a version of the video
        self.version_control.append((len(self.version_control) + 1, datetime.now()))
        print("Version saved.")

    def revert_version(self, version_number):
        # Simulate reverting to a previous version of the video
        if version_number <= len(self.version_control):
            print(f"Reverted to version {version_number}.")
        else:
            print("Invalid version number.")

    def display_chat_log(self):
        for message in self.chat_log:
            print(f"{message[0]} at {message[2]}: {message[1]}")

    def display_version_control(self):
        for version in self.version_control:
            print(f"Version {version[0]} saved at {version[1]}")


class User:
    def __init__(self, name):
        self.name = name

    def send_message(self, suite, message):
        suite.send_message(self.name, message)


def main():
    suite = VideoCollaborationSuite()

    user1 = User("John")
    user2 = User("Jane")

    suite.add_user(user1)
    suite.add_user(user2)

    suite.upload_video("video.mp4")
    suite.upload_subtitle("subtitle.srt")

    suite.sync_subtitles()

    user1.send_message(suite, "Hello, Jane!")
    user2.send_message(suite, "Hi, John!")

    suite.adjust_playback_speed(1.5)

    suite.save_version()

    suite.revert_version(1)

    suite.display_chat_log()
    suite.display_version_control()


if __name__ == "__main__":
    main()