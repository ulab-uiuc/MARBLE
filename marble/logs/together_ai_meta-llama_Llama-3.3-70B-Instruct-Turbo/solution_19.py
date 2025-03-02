# user_registration.py
class User:
    def __init__(self, username, email, password):
        # Initialize user object with username, email, and password
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        # Return a string representation of the user
        return f"User('{self.username}', '{self.email}')"


class UserRegistration:def register_user(self, username, email, password):
    def __init__(self):
        self.users = {}
    import bcrypt
    if username in self.users or email in [user.email for user in self.users.values()]:
        print("Username or email already taken.")
    else:
        self.users[username] = User(username, email, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
        print(f"User '{username}' registered successfully.")def login_user(self, username, password):if username in self.users and bcrypt.checkpw(password.encode('utf-8'), self.users[username].password):print(f"User '{username}' logged in successfully.")
            return self.users[username]
        else:
            print("Invalid username or password.")
            return None


# story_creation.py
class Story:
    def __init__(self, title, content, author):
        # Initialize story object with title, content, and author
        self.title = title
        self.content = content
        self.author = author
        self.chapters = []
        self.versions = [content]

    def add_chapter(self, chapter):
        # Add a new chapter to the story
        self.chapters.append(chapter)

    def edit_content(self, new_content):
        # Edit the story content and add a new version
        self.content = new_content
        self.versions.append(new_content)

    def __str__(self):
        # Return a string representation of the story
        return f"Story('{self.title}', '{self.author}')"


class StoryCreation:
    def __init__(self):
        # Initialize an empty dictionary to store created stories
        self.stories = {}

    def create_story(self, title, content, author):
        # Create a new story if the title is not already taken
        if title not in self.stories:
            self.stories[title] = Story(title, content, author)
            print(f"Story '{title}' created successfully.")
        else:
            print("Story title already taken.")

    def get_story(self, title):
        # Get a story by its title
        return self.stories.get(title)


# real_time_collaboration.py
import threading

class RealTimeCollaboration:
    def __init__(self):
        # Initialize a lock for thread-safe editing
        self.lock = threading.Lock()

    def edit_story(self, story, new_content):
        # Edit a story in real-time using a lock for thread safety
        with self.lock:
            story.edit_content(new_content)


# version_control.py
class VersionControl:
    def __init__(self):
        # Initialize an empty dictionary to store story versions
        self.versions = {}

    def add_version(self, story, version):
        # Add a new version to the story's version history
        if story.title not in self.versions:
            self.versions[story.title] = [version]
        else:
            self.versions[story.title].append(version)

    def get_versions(self, story):
        # Get all versions of a story
        return self.versions.get(story.title, [])


# community_gallery.py
class CommunityGallery:
    def __init__(self):
        # Initialize an empty dictionary to store stories in the gallery
        self.gallery = {}

    def add_story(self, story):
        # Add a story to the community gallery
        self.gallery[story.title] = story

    def get_stories(self):
        # Get all stories in the community gallery
        return list(self.gallery.values())


# notification_system.py
class NotificationSystem:
    def __init__(self):
        # Initialize an empty dictionary to store user notifications
        self.notifications = {}

    def add_notification(self, user, notification):
        # Add a new notification to a user's notification list
        if user.username not in self.notifications:
            self.notifications[user.username] = [notification]
        else:
            self.notifications[user.username].append(notification)

    def get_notifications(self, user):
        # Get all notifications for a user
        return self.notifications.get(user.username, [])


# CollaborativeStoryBuilder.py
class CollaborativeStoryBuilder:
    def __init__(self):
        # Initialize all components of the Collaborative Story Builder
        self.user_registration = UserRegistration()
        self.story_creation = StoryCreation()
        self.real_time_collaboration = RealTimeCollaboration()
        self.version_control = VersionControl()
        self.community_gallery = CommunityGallery()
        self.notification_system = NotificationSystem()

    def run(self):
        # Run the Collaborative Story Builder
        while True:
            print("1. Register User")
            print("2. Login User")
            print("3. Create Story")
            print("4. Edit Story")
            print("5. Add Chapter")
            print("6. View Story")
            print("7. View Versions")
            print("8. Add to Gallery")
            print("9. View Gallery")
            print("10. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                username = input("Enter username: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                self.user_registration.register_user(username, email, password)
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.user_registration.login_user(username, password)
                if user:
                    print(f"Welcome, {user.username}!")
            elif choice == "3":
                title = input("Enter story title: ")
                content = input("Enter story content: ")
                author = input("Enter author name: ")
                self.story_creation.create_story(title, content, author)
            elif choice == "4":
                title = input("Enter story title: ")
                new_content = input("Enter new story content: ")
                story = self.story_creation.get_story(title)
                if story:
                    self.real_time_collaboration.edit_story(story, new_content)
                    self.version_control.add_version(story, new_content)
                else:
                    print("Story not found.")
            elif choice == "5":
                title = input("Enter story title: ")
                chapter = input("Enter chapter content: ")
                story = self.story_creation.get_story(title)
                if story:
                    story.add_chapter(chapter)
                else:
                    print("Story not found.")
            elif choice == "6":
                title = input("Enter story title: ")
                story = self.story_creation.get_story(title)
                if story:
                    print(story.content)
                else:
                    print("Story not found.")
            elif choice == "7":
                title = input("Enter story title: ")
                story = self.story_creation.get_story(title)
                if story:
                    versions = self.version_control.get_versions(story)
                    for version in versions:
                        print(version)
                else:
                    print("Story not found.")
            elif choice == "8":
                title = input("Enter story title: ")
                story = self.story_creation.get_story(title)
                if story:
                    self.community_gallery.add_story(story)
                else:
                    print("Story not found.")
            elif choice == "9":
                stories = self.community_gallery.get_stories()
                for story in stories:
                    print(story.title)
            elif choice == "10":
                break
            else:
                print("Invalid option. Please choose again.")

if __name__ == "__main__":
    builder = CollaborativeStoryBuilder()
    builder.run()