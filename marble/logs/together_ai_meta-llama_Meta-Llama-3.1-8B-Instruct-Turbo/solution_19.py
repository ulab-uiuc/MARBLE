# user.py
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.stories = []

    def create_story(self, story_id):
        self.stories.append(Story(story_id, self.id))

    def edit_story(self, story_id, chapter_id, content):
        for story in self.stories:
            if story.id == story_id:
                story.edit_chapter(chapter_id, content)
                return

    def get_story(self, story_id):
        for story in self.stories:
            if story.id == story_id:
                return story
        return None


class Story:
    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id
        self.chapters = {}

    def add_chapter(self, chapter_id, content):
        self.chapters[chapter_id] = Chapter(chapter_id, content)

    def edit_chapter(self, chapter_id, content):
        if chapter_id in self.chapters:
            self.chapters[chapter_id].content = content

    def get_chapter(self, chapter_id):
        return self.chapters.get(chapter_id)


class Chapter:
    def __init__(self, id, content):
        self.id = id
        self.content = content


# story.py
class StoryService:
    def __init__(self):
        self.stories = {}

    def create_story(self, user_id, story_id):
        if user_id not in self.stories:
            self.stories[user_id] = {}
        self.stories[user_id][story_id] = Story(story_id, user_id)

    def edit_story(self, user_id, story_id, chapter_id, content):
        if user_id in self.stories and story_id in self.stories[user_id]:
            self.stories[user_id][story_id].edit_chapter(chapter_id, content)

    def get_story(self, user_id, story_id):
        return self.stories.get(user_id, {}).get(story_id)


# version_control.py
class VersionControl:
    def __init__(self):
        self.versions = {}

    def create_version(self, story_id, user_id, version_number, content):
        if story_id not in self.versions:
            self.versions[story_id] = {}
        self.versions[story_id][version_number] = {
            'user_id': user_id,
            'content': content
        }

    def get_version(self, story_id, version_number):
        return self.versions.get(story_id, {}).get(version_number)


# community_gallery.py
class CommunityGallery:
    def __init__(self):
        self.stories = {}

    def add_story(self, story_id, user_id, title, content):
        self.stories[story_id] = {
            'user_id': user_id,
            'title': title,
            'content': content
        }

    def get_story(self, story_id):
        return self.stories.get(story_id)


# notification_system.py
class NotificationSystem:
    def __init__(self):
        self.notifications = {}

    def send_notification(self, user_id, story_id, notification_type):
        if user_id not in self.notifications:
            self.notifications[user_id] = []
        self.notifications[user_id].append({
            'story_id': story_id,
            'notification_type': notification_type
        })

    def get_notifications(self, user_id):
        return self.notifications.get(user_id, [])


# solution.py
class CollaborativeStoryBuilder:
    def __init__(self):
        self.user_service = UserService()
        self.story_service = StoryService()
        self.version_control = VersionControl()
        self.community_gallery = CommunityGallery()
        self.notification_system = NotificationSystem()

    def register_user(self, username, password):
        self.user_service.create_user(username, password)

    def login_user(self, username, password):
        return self.user_service.login_user(username, password)

    def create_story(self, user_id, story_id):
        self.story_service.create_story(user_id, story_id)

    def edit_story(self, user_id, story_id, chapter_id, content):
        self.story_service.edit_story(user_id, story_id, chapter_id, content)
        self.version_control.create_version(story_id, user_id, 1, content)

    def get_story(self, user_id, story_id):
        return self.story_service.get_story(user_id, story_id)

    def add_story_to_gallery(self, story_id, user_id, title, content):
        self.community_gallery.add_story(story_id, user_id, title, content)

    def get_story_from_gallery(self, story_id):
        return self.community_gallery.get_story(story_id)

    def send_notification(self, user_id, story_id, notification_type):
        self.notification_system.send_notification(user_id, story_id, notification_type)


class UserService:
    def __init__(self):
        self.users = {}

    def create_user(self, username, password):
        self.users[username] = User(len(self.users) + 1, username, password)

    def login_user(self, username, password):
        if username in self.users:
            return self.users[username]
        return None


# Usage
if __name__ == "__main__":
    builder = CollaborativeStoryBuilder()

    # Register user
    builder.register_user('john', 'password123')

    # Login user
    user = builder.login_user('john', 'password123')

    # Create story
    builder.create_story(user.id, 1)

    # Edit story
    builder.edit_story(user.id, 1, 1, 'New content')

    # Get story
    story = builder.get_story(user.id, 1)
    print(story.get_chapter(1).content)

    # Add story to gallery
    builder.add_story_to_gallery(1, user.id, 'My Story', 'This is my story')

    # Get story from gallery
    story_from_gallery = builder.get_story_from_gallery(1)
    print(story_from_gallery['title'])

    # Send notification
    builder.send_notification(user.id, 1, 'new contribution')