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
    def __init__(self, title: str, format: str):
        self.title = title
        self.format = format
        self.history: List[EditAction] = []
        self.current_state = None

    def apply_edit(self, action: EditAction):
        # Apply the edit action to the video
        self.history.append(action)
        self.current_state = action.details  # Simplified for demonstration

    def undo(self):
        # Undo the last action
        if self.history:
            self.history.pop()
            self.current_state = self.history[-1].details if self.history else None

    def redo(self):
        # Redo the last undone action (not implemented for simplicity)
        pass

# Define a class for the collaborative video editor
class VideoCollabEditor:
    def __init__(self):
        self.users: List[User] = []
        self.video: Video = None
        self.feedback: List[str] = []

    def add_user(self, user: User):
        self.users.append(user)

    def create_video(self, title: str, format: str):
        self.video = Video(title, format)

    def edit_video(self, action: EditAction, user: User):
        # Check user permissions
        if user.role in [UserRole.OWNER, UserRole.EDITOR]:
            self.video.apply_edit(action)
            self.sync_changes(action)
        else:
            raise PermissionError("User does not have permission to edit the video.")

    def sync_changes(self, action: EditAction):
        # Simulate real-time synchronization of changes to all users
        print(f"Syncing changes: {json.dumps(action.details)} to all users.")

    def provide_feedback(self, comment: str):
        self.feedback.append(comment)

    def review_feedback(self):
        # Review feedback (not implemented for simplicity)
        pass

    def export_video(self, format: str):
        # Export the video in the specified format (not implemented for simplicity)
        print(f"Exporting video '{self.video.title}' in format '{format}'.")

# Example usage
if __name__ == "__main__":
    editor = VideoCollabEditor()
    
    # Create users
    owner = User("Alice", UserRole.OWNER)
    editor_user = User("Bob", UserRole.EDITOR)
    reviewer = User("Charlie", UserRole.REVIEWER)

    # Add users to the editor
    editor.add_user(owner)
    editor.add_user(editor_user)
    editor.add_user(reviewer)

    # Create a new video
    editor.create_video("My First Video", "mp4")

    # Perform an edit action
    cut_action = EditAction("cut", {"start": 0, "end": 10})
    editor.edit_video(cut_action, editor_user)

    # Provide feedback
    editor.provide_feedback("Consider adding a transition here.")

    # Export the video
    editor.export_video("mp4")