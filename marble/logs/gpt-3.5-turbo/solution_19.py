# CollaborativeStoryBuilder.py

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.stories = []

    def create_story(self, title):
        new_story = Story(title)
        self.stories.append(new_story)
        return new_story

class Story:
    def __init__(self, title):
        self.title = title
        self.chapters = []
        self.current_version = 1
        self.versions = {1: ""}

    def add_chapter(self, content):
        self.chapters.append(content)

    def edit_chapter(self, chapter_num, new_content):    def save_version(self):
        if version_num in self.versions:        if version_num in self.versions:
        if version_num in self.versions:
            self.chapters = self.versions[version_num]
        else:            raise ValueError('Version number not found')            self.chapters = self.versions[version_num]
        else:
            raise ValueError('Version number not found')        if version_num in self.versions:
            self.chapters = self.versions[version_num]
        else:
            raise ValueError("Version number not found")

class CommunityGallery:
    def __init__(self):
        self.stories = []

    def add_story(self, story):
        self.stories.append(story)

    def browse_stories(self):
        return self.stories

class NotificationSystem:
    def __init__(self):
        self.notifications = []

    def send_notification(self, message):
        self.notifications.append(message)

# User Registration and Authentication
user1 = User("Alice", "alice@example.com", "password123")
user2 = User("Bob", "bob@example.com", "password456")

# Story Creation and Editing
story1 = user1.create_story("The Adventure Begins")
story1.add_chapter("Chapter 1: Once upon a time...")
story1.add_chapter("Chapter 2: The hero's journey...")

story1.edit_chapter(2, "Chapter 2: The hero's journey continues...")

story1.save_version()

# Real-Time Collaboration
user2_story1 = user2.stories[0]
user2_story1.edit_chapter(2, "Chapter 2: The hero's journey takes a twist...")

# Version Control
user2_story1.save_version()
user2_story1.revert_to_version(1)

# Community Gallery
gallery = CommunityGallery()
gallery.add_story(story1)
stories = gallery.browse_stories()

# Notification System
notification_system = NotificationSystem()
notification_system.send_notification("New comment on your story!")

# Additional features and functionalities can be added as needed