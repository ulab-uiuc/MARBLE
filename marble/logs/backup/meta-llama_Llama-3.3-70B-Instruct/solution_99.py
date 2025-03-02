def undo(self):
        if self.history:
            last_state = self.history.pop()
            self.features = last_state['features']
            self.format = last_state['format']
            self.undone.append(last_state)# solution.py
import threading
from enum import Enum
from typing import List, Dict

# Define user roles
class UserRole(Enum):
    """User roles with corresponding permissions"""
    OWNER = 1
    EDITOR = 2
    REVIEWER = 3

# Define video editing features
class VideoFeature(Enum):
    """Video editing features"""
    CUT = 1
    CROP = 2
    RESIZE = 3
    FILTER = 4

# Define video formats
class VideoFormat(Enum):
    """Video formats"""
    MP4 = 1
    AVI = 2
    MOV = 3

# User class
class User:
    """User with role and permissions"""
    def __init__(self, name: str, role: UserRole):
        self.name = name
        self.role = role

# Video class
class Video:
    """Video with editing features and history"""
    def __init__(self, name: str, format: VideoFormat):
    def add_feature(self, feature: VideoFeature):
        self.features.append(feature)
        self.name = name
        self.format = format
        self.history = []
        self.features = []def undo(self):
        if self.history:
            last_state = self.history.pop()
            self.features = last_state['features']
            self.format = last_state['format']
            self.undone.append(last_state)
    def redo(self):
        """Redo last undone action"""
        # Not implemented for simplicity

# VideoCollabEditor class
class VideoCollabEditor:
    """Collaborative video editing system"""
    def __init__(self):
        self.videos = {}
        self.users = {}
        self.lock = threading.Lock()

    def add_user(self, user: User):
        """Add user to the system"""
        with self.lock:
            self.users[user.name] = user

    def add_video(self, video: Video):
        """Add video to the system"""
        with self.lock:
            self.videos[video.name] = video

    def edit_video(self, user_name: str, video_name: str, feature: VideoFeature):
        """Edit video with given feature"""
        with self.lock:
            user = self.users.get(user_name)
            video = self.videos.get(video_name)
            if user and video:
                # Check user permissions
                if user.role == UserRole.OWNER or user.role == UserRole.EDITOR:
                    video.add_feature(feature)
                    video.history.append(feature)
                else:
                    print("User does not have permission to edit the video")

    def provide_feedback(self, user_name: str, video_name: str, feedback: str):
        """Provide feedback on a video"""
        with self.lock:
            user = self.users.get(user_name)
            video = self.videos.get(video_name)
            if user and video:
                # Check user permissions
                if user.role == UserRole.REVIEWER:
                    print(f"Feedback from {user_name} on {video_name}: {feedback}")
                else:
                    print("User does not have permission to provide feedback")

    def export_video(self, video_name: str, format: VideoFormat):
        """Export video in given format"""
        with self.lock:
            video = self.videos.get(video_name)
            if video:
                # Check if format is supported
                if format in [VideoFormat.MP4, VideoFormat.AVI, VideoFormat.MOV]:
                    print(f"Exporting {video_name} in {format.name} format")
                else:
                    print("Unsupported format")

# Example usage
if __name__ == "__main__":
    editor = VideoCollabEditor()

    # Create users
    user1 = User("John", UserRole.OWNER)
    user2 = User("Jane", UserRole.EDITOR)
    user3 = User("Bob", UserRole.REVIEWER)

    # Add users to the system
    editor.add_user(user1)
    editor.add_user(user2)
    editor.add_user(user3)

    # Create video
    video1 = Video("Video1", VideoFormat.MP4)

    # Add video to the system
    editor.add_video(video1)

    # Edit video
    editor.edit_video("John", "Video1", VideoFeature.CUT)
    editor.edit_video("Jane", "Video1", VideoFeature.CROP)

    # Provide feedback
    editor.provide_feedback("Bob", "Video1", "Good job!")

    # Export video
    editor.export_video("Video1", VideoFormat.AVI)