# user.py
class User:
    def __init__(self, username, email, password):
        """
        Initialize a User object.

        Args:
            username (str): The username chosen by the user.
            email (str): The email address of the user.
            password (str): The password chosen by the user.
        """
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        """
        Return a string representation of the User object.

        Returns:
            str: A string containing the username and email.
        """
        return f"Username: {self.username}, Email: {self.email}"


# story.py
class Story:
    def __init__(self, title, author):
        """
        Initialize a Story object.

        Args:
            title (str): The title of the story.
            author (User): The author of the story.
        """
        self.title = title
        self.author = author
        self.chapters = []
        self.versions = []

    def add_chapter(self, chapter):
        """
        Add a chapter to the story.

        Args:
            chapter (str): The chapter to be added.
        """
        self.chapters.append(chapter)

    def edit_chapter(self, chapter_index, new_chapter):
        """
        Edit a chapter in the story.

        Args:
            chapter_index (int): The index of the chapter to be edited.
            new_chapter (str): The new chapter content.
        """
        if chapter_index < len(self.chapters):
            self.chapters[chapter_index] = new_chapter

    def add_version(self, version):
        """
        Add a version to the story.

        Args:
            version (str): The version to be added.
        """
        self.versions.append(version)


# collaborative_story_builder.py
class CollaborativeStoryBuilder:
    def __init__(self):
        """
        Initialize a CollaborativeStoryBuilder object.
        """
        self.users = []
        self.stories = []

    def register_user(self, username, email, password):
        """
        Register a new user.

        Args:
            username (str): The username chosen by the user.
            email (str): The email address of the user.
            password (str): The password chosen by the user.
        """
        new_user = User(username, email, password)
        self.users.append(new_user)

    def create_story(self, title, author):
        """
        Create a new story.

        Args:
            title (str): The title of the story.
            author (User): The author of the story.
        """
        new_story = Story(title, author)
        self.stories.append(new_story)

    def add_collaborator(self, story_title, collaborator):
        """
        Add a collaborator to a story.

        Args:
            story_title (str): The title of the story.
            collaborator (User): The collaborator to be added.
        """
        for story in self.stories:
            if story.title == story_title:
                # Add collaborator to the story (not implemented)
                pass

    def edit_story(self, story_title, chapter_index, new_chapter):
        """
        Edit a story.

        Args:
            story_title (str): The title of the story.
            chapter_index (int): The index of the chapter to be edited.
            new_chapter (str): The new chapter content.
        """
        for story in self.stories:
            if story.title == story_title:
                story.edit_chapter(chapter_index, new_chapter)

    def add_version(self, story_title, version):
        """
        Add a version to a story.

        Args:
            story_title (str): The title of the story.
            version (str): The version to be added.
        """
        for story in self.stories:
            if story.title == story_title:
                story.add_version(version)

    def display_stories(self):
        """
        Display all stories.
        """
        for story in self.stories:
            print(f"Title: {story.title}, Author: {story.author}")


# community_gallery.py
class CommunityGallery:
    def __init__(self):
        """
        Initialize a CommunityGallery object.
        """
        self.stories = []

    def add_story(self, story):
        """
        Add a story to the community gallery.

        Args:
            story (Story): The story to be added.
        """
        self.stories.append(story)

    def display_stories(self):
        """
        Display all stories in the community gallery.
        """
        for story in self.stories:
            print(f"Title: {story.title}, Author: {story.author}")


# notification_system.py
class NotificationSystem:
    def __init__(self):
        """
        Initialize a NotificationSystem object.
        """
        self.notifications = []

    def add_notification(self, notification):
        """
        Add a notification to the system.

        Args:
            notification (str): The notification to be added.
        """
        self.notifications.append(notification)

    def display_notifications(self):
        """
        Display all notifications.
        """
        for notification in self.notifications:
            print(notification)


# main.py
def main():
    # Create a CollaborativeStoryBuilder object
    csb = CollaborativeStoryBuilder()

    # Register users
    csb.register_user("user1", "user1@example.com", "password1")
    csb.register_user("user2", "user2@example.com", "password2")

    # Create stories
    user1 = next((user for user in csb.users if user.username == "user1"), None)
    csb.create_story("Story 1", user1)
    csb.create_story("Story 2", user1)

    # Add collaborators
    user2 = next((user for user in csb.users if user.username == "user2"), None)
    csb.add_collaborator("Story 1", user2)

    # Edit stories
    csb.edit_story("Story 1", 0, "New chapter content")

    # Add versions
    csb.add_version("Story 1", "Version 1")

    # Display stories
    csb.display_stories()

    # Create a CommunityGallery object
    gallery = CommunityGallery()

    # Add stories to the community gallery
    story1 = next((story for story in csb.stories if story.title == "Story 1"), None)
    gallery.add_story(story1)

    # Display stories in the community gallery
    gallery.display_stories()

    # Create a NotificationSystem object
    notification_system = NotificationSystem()

    # Add notifications
    notification_system.add_notification("New contribution to Story 1")
    notification_system.add_notification("New comment on Story 1")

    # Display notifications
    notification_system.display_notifications()


if __name__ == "__main__":
    main()