# solution.py

# Import necessary libraries
from typing import List, Dict, Any
import json

# Define user roles
class UserRole:
    OWNER = "owner"
    EDITOR = "editor"
    REVIEWER = "reviewer"

# Define a class to represent a user in the system
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

# Define a class to represent a video editing action
class EditAction:
    def __init__(self, action_type: str, details: Dict[str, Any]):
        self.action_type = action_type
        self.details = details

# Define a class to represent a video
class Video:
    def __init__(self, title: str, format: str, resolution: str):
        self.title = title
        self.format = format
        self.resolution = resolution
        self.edit_history: List[EditAction] = []
        self.current_version: int = 0

    def add_edit(self, action: EditAction):
        """Add an edit action to the video and increment the version."""
        self.edit_history.append(action)
        self.current_version += 1

    def get_edit_history(self) -> List[EditAction]:
        """Return the history of edits."""
        return self.edit_history

# Define a class for the collaborative video editor
class VideoCollabEditor:
    def __init__(self):
        self.videos: Dict[str, Video] = {}
        self.users: Dict[str, User] = {}
        self.feedback: Dict[str, List[str]] = {}def edit_video(self, title: str, action: EditAction, username: str):
        """Edit a video if the user has the right permissions."""
        video = self.videos.get(title)
        user = self.users.get(username)

        if video and user:
            if user.role in [UserRole.OWNER, UserRole.EDITOR]:
                video.add_edit(action)
                self.sync_changes(title)
                self.undo_stack.append(action)
                self.redo_stack.clear()  # Clear redo stack on new action
            else:
                raise PermissionError("User does not have permission to edit this video.")    def sync_changes(self, title: str):
        """Sync changes to all users (placeholder for real-time sync)."""
        print(f"Changes to video '{title}' have been synced to all users.")

    def provide_feedback(self, title: str, feedback: str, username: str):
        """Allow users to provide feedback on a video."""
        if title not in self.feedback:
            self.feedback[title] = []
        self.feedback[title].append(f"{username}: {feedback}")

    def get_feedback(self, title: str) -> List[str]:
        """Retrieve feedback for a specific video."""
        return self.feedback.get(title, [])

    def export_video(self, title: str, export_format: str):
        """Export the video in the specified format (placeholder)."""
        print(f"Exporting video '{title}' in format '{export_format}'.")

# Example usage
if __name__ == "__main__":
    editor = VideoCollabEditor()
    
    # Adding users
    editor.add_user("alice", UserRole.OWNER)
    editor.add_user("bob", UserRole.EDITOR)
    editor.add_user("charlie", UserRole.REVIEWER)

    # Creating a video
    editor.create_video("My First Video", "mp4", "1920x1080")

    # Editing the video
    editor.edit_video("My First Video", EditAction("cut", {"start": 0, "end": 10}), "alice")
    editor.edit_video("My First Video", EditAction("crop", {"width": 800, "height": 600}), "bob")

    # Providing feedback
    editor.provide_feedback("My First Video", "Great editing!", "charlie")

    # Retrieving feedback
    feedback = editor.get_feedback("My First Video")
    print("Feedback for 'My First Video':", feedback)

    # Exporting the video
    editor.export_video("My First Video", "mp4")