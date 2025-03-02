# user.py
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.stories = []

    def __str__(self):
        return f"User {self.username}"

# story.py
class Story:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author
        self.chapters = []
        self.version_history = []

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def update_version(self, new_version):
        self.version_history.append(new_version)

    def __str__(self):
        return f"Story {self.title} by {self.author}"

# chapter.py
class Chapter:
    def __init__(self, id, content):
        self.id = id
        self.content = content

    def __str__(self):
        return f"Chapter {self.id}: {self.content}"

# collaborative_story_builder.py
class CollaborativeStoryBuilder:
    def __init__(self):
        self.users = {}
        self.stories = {}

    def register_user(self, username, password):
        if username not in self.users:
            self.users[username] = User(len(self.users) + 1, username, password)
            return self.users[username]
        else:
            return None

    def login_user(self, username, password):
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            return None

    def create_story(self, title, author):
        if author in self.users:
            if title not in self.stories:
                self.stories[title] = Story(len(self.stories) + 1, title, author)
                return self.stories[title]
            else:
                return None
        else:
            return None

    def add_chapter(self, story_title, chapter_content):
        if story_title in self.stories:
            self.stories[story_title].add_chapter(Chapter(len(self.stories[story_title].chapters) + 1, chapter_content))
            return self.stories[story_title]
        else:
            return None

    def update_story_version(self, story_title, new_version):
        if story_title in self.stories:
            self.stories[story_title].update_version(new_version)
            return self.stories[story_title]
        else:
            return None

    def get_story(self, story_title):
        if story_title in self.stories:
            return self.stories[story_title]
        else:
            return None

    def get_user_stories(self, username):
        if username in self.users:
            return self.users[username].stories
        else:
            return None

# solution.py
class Solution:
    def __init__(self):
        self.collaborative_story_builder = CollaborativeStoryBuilder()

    def run(self):
        # Register a user
        user1 = self.collaborative_story_builder.register_user("john_doe", "password123")
        print(user1)

        # Login a user
        logged_in_user = self.collaborative_story_builder.login_user("john_doe", "password123")
        print(logged_in_user)

        # Create a story
        story1 = self.collaborative_story_builder.create_story("My Story", "john_doe")
        print(story1)

        # Add a chapter to the story
        self.collaborative_story_builder.add_chapter("My Story", "This is the first chapter.")
        print(self.collaborative_story_builder.get_story("My Story"))

        # Update the story version
        self.collaborative_story_builder.update_story_version("My Story", "This is the updated version.")
        print(self.collaborative_story_builder.get_story("My Story"))

        # Get the user's stories
        user_stories = self.collaborative_story_builder.get_user_stories("john_doe")
        print(user_stories)

if __name__ == "__main__":
    solution = Solution()
    solution.run()