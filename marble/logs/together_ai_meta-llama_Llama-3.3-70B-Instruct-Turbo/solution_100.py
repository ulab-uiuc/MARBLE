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
        self.version_control = []
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
            print("Manually adjusting subtitles...")
            time.sleep(1)  # Simulate processing time
            print("Subtitles adjusted successfully.")

    # Method to adjust playback speed
    def adjust_playback_speed(self, speed):
        # Acquire lock for synchronization
        with self.lock:
            self.playback_speed = speed
            print(f"Playback speed adjusted to {speed}x.")

    # Method to send chat message
    def send_chat_message(self, message):
        # Acquire lock for synchronization
        with self.lock:
            self.chat_log.append((datetime.now(), message))
            print(f"Chat message sent: {message}")

    # Method to save versiondef revert_version(self, version_name):
        # Acquire lock for synchronization
        with self.lock:
            for version in self.version_control:
                if version[0] == version_name:
                    self.video_file = version[1]
                    self.subtitle_file = version[2]
                    self.playback_speed = version[3]
                    # Update chat log to match the reverted version
                    self.chat_log = [log for log in self.chat_log if log[0] <= version[4]]
                    print(f"Reverted to version: {version_name}")
                    return
            # Handle the case where the version is not found
            raise ValueError(f"Version '{version_name}' not found.")        for version in self.version_control:
                if version[0] == version_name:
                    self.video_file = version[1]
                    self.subtitle_file = version[2]
                    self.playback_speed = version[3]
                    print(f"Reverted to version: {version_name}")
                    return
            print("Version not found.")

# User class
class User:
    def __init__(self, name, video_collaboration_suite):
        self.name = name
        self.video_collaboration_suite = video_collaboration_suite

    # Method to upload files
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

    # Method to send chat message
    def send_chat_message(self, message):
        print(f"{self.name} is sending chat message...")
        self.video_collaboration_suite.send_chat_message(message)

    # Method to save version
    def save_version(self, version_name):
        print(f"{self.name} is saving version...")
        self.video_collaboration_suite.save_version(version_name)

    # Method to revert version
    def revert_version(self, version_name):
        print(f"{self.name} is reverting version...")
        self.video_collaboration_suite.revert_version(version_name)

# Main function
def main():
    video_collaboration_suite = VideoCollaborationSuite()
    user1 = User("John", video_collaboration_suite)
    user2 = User("Jane", video_collaboration_suite)

    # Simulate collaborative editing
    user1.upload_files("video.mp4", "subtitles.srt")
    user2.synchronize_subtitles()
    user1.adjust_subtitles("adjustment")
    user2.adjust_playback_speed(1.5)
    user1.send_chat_message("Hello, Jane!")
    user2.save_version("version1")
    user1.revert_version("version1")

if __name__ == "__main__":
    main()