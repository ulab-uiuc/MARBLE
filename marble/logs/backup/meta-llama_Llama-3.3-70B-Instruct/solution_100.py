# solution.py
import threading
from datetime import datetime
import time

# VideoCollaborationSuite class
class VideoCollaborationSuite:
    def __init__(self):
        # Initialize video and subtitle files
        self.video_file = None
        self.subtitle_file = None
        # Initialize playback speed
        self.playback_speed = 1.0
        # Initialize chat log
        self.chat_log = []
        # Initialize version control
        self.versions = []
        # Initialize lock for synchronization
        self.lock = threading.Lock()

    # Method to upload video and subtitle files
    def upload_files(self, video_file, subtitle_file):
        # Acquire lock for synchronization
        with self.lock:
            self.video_file = video_file
            self.subtitle_file = subtitle_file
            print("Video and subtitle files uploaded successfully.")

    # Method for automatic subtitle synchronization
    def synchronize_subtitles(self):
        # Acquire lock for synchronization
        with self.lock:
            # Simulate automatic subtitle synchronization
            print("Automatic subtitle synchronization in progress...")
            time.sleep(2)  # Simulate processing time
            print("Subtitles synchronized successfully.")

    # Method to manually adjust subtitle synchronization
    def adjust_subtitles(self, adjustment):
        # Acquire lock for synchronization
        with self.lock:
            # Simulate manual subtitle adjustment
            print(f"Adjusting subtitles by {adjustment} seconds...")
            time.sleep(1)  # Simulate processing time
            print("Subtitles adjusted successfully.")

    # Method to adjust playback speed
    def adjust_playback_speed(self, speed):
        # Acquire lock for synchronization
        with self.lock:
            self.playback_speed = speed
            print(f"Playback speed adjusted to {speed}x.")

    # Method to send a chat message
    def send_message(self, message):
        # Acquire lock for synchronization
        with self.lock:
            self.chat_log.append((datetime.now(), message))
            print(f"Message sent: {message}")

    # Method to save a version of the video
    def save_version(self, version_name):self.versions.append({'version_id': len(self.versions) + 1, 'version_name': version_name, 'video_file': self.video_file, 'subtitle_file': self.subtitle_file, 'playback_speed': self.playback_speed, 'chat_log': self.chat_log, 'timestamp': datetime.now()})print(f"Version saved: {version_name}")

    # Method to revert to a previous version
    def revert_version(self, version_name):with self.lock:
            for version in self.versions:
        if not any(version['version_name'] == version_name for version in self.versions):
            print('Version not found.')
            return
                if version['version_name'] == version_name and version['version_id'] == max([v['version_id'] for v in self.versions if v['version_name'] == version_name]):self.video_file = version['video_file']
                self.subtitle_file = version['subtitle_file']
                self.playback_speed = version['playback_speed']
                self.chat_log = version['chat_log']print(f"Reverted to version: {version_name}")
                    return
            print("Version not found.")

# User class
class User:
    def __init__(self, name, video_collaboration_suite):
        self.name = name
        self.video_collaboration_suite = video_collaboration_suite

    # Method to upload video and subtitle files
    def upload_files(self, video_file, subtitle_file):
        print(f"{self.name} is uploading files...")
        self.video_collaboration_suite.upload_files(video_file, subtitle_file)

    # Method to synchronize subtitles
    def synchronize_subtitles(self):
        print(f"{self.name} is synchronizing subtitles...")
        self.video_collaboration_suite.synchronize_subtitles()

    # Method to adjust subtitles
    def adjust_subtitles(self, adjustment):
        print(f"{self.name} is adjusting subtitles...")
        self.video_collaboration_suite.adjust_subtitles(adjustment)

    # Method to adjust playback speed
    def adjust_playback_speed(self, speed):
        print(f"{self.name} is adjusting playback speed...")
        self.video_collaboration_suite.adjust_playback_speed(speed)

    # Method to send a chat message
    def send_message(self, message):
        print(f"{self.name} is sending a message...")
        self.video_collaboration_suite.send_message(message)

    # Method to save a version of the video
    def save_version(self, version_name):
        print(f"{self.name} is saving a version...")
        self.video_collaboration_suite.save_version(version_name)

    # Method to revert to a previous version
    def revert_version(self, version_name):
        print(f"{self.name} is reverting to a version...")
        self.video_collaboration_suite.revert_version(version_name)

# Main function
def main():
    # Create a VideoCollaborationSuite instance
    video_collaboration_suite = VideoCollaborationSuite()

    # Create user instances
    user1 = User("John", video_collaboration_suite)
    user2 = User("Jane", video_collaboration_suite)

    # Upload video and subtitle files
    user1.upload_files("video.mp4", "subtitles.srt")

    # Synchronize subtitles
    user1.synchronize_subtitles()

    # Adjust subtitles
    user2.adjust_subtitles(1.5)

    # Adjust playback speed
    user1.adjust_playback_speed(1.5)

    # Send chat messages
    user1.send_message("Hello, Jane!")
    user2.send_message("Hi, John!")

    # Save versions of the video
    user1.save_version("Version 1")
    user2.save_version("Version 2")

    # Revert to a previous version
    user1.revert_version("Version 1")

if __name__ == "__main__":
    main()