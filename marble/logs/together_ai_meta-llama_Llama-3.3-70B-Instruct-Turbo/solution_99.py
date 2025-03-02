# solution.py
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
        self.name = name
        self.format = format
        self.history = []
        self.features = []def undo(self):
        """Undo last action"""
        if self.history:
            self.undone_actions.append(self.history.pop())
    def redo(self):
        """Redo last undone action"""
        # Implement redo functionality
        pass

# VideoCollabEditor class
class VideoCollabEditor:
    """Collaborative video editing system"""
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.videos: Dict[str, Video] = {}
        self.lock = threading.Lock()

    def add_user(self, name: str, role: UserRole):
        """Add user to the system"""
        with self.lock:
            self.users[name] = User(name, role)

    def add_video(self, name: str, format: VideoFormat):
        """Add video to the system"""
        with self.lock:
            self.videos[name] = Video(name, format)

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
                # Check if video format is supported
                if format in [VideoFormat.MP4, VideoFormat.AVI, VideoFormat.MOV]:
                    print(f"Exporting {video_name} in {format} format")
                else:
                    print("Unsupported video format")

# Usage example
if __name__ == "__main__":
    editor = VideoCollabEditor()

    # Add users
    editor.add_user("John", UserRole.OWNER)
    editor.add_user("Alice", UserRole.EDITOR)
    editor.add_user("Bob", UserRole.REVIEWER)

    # Add video
    editor.add_video("My Video", VideoFormat.MP4)

    # Edit video
    editor.edit_video("John", "My Video", VideoFeature.CUT)
    editor.edit_video("Alice", "My Video", VideoFeature.CROP)

    # Provide feedback
    editor.provide_feedback("Bob", "My Video", "Good job!")

    # Export video
    editor.export_video("My Video", VideoFormat.AVI)