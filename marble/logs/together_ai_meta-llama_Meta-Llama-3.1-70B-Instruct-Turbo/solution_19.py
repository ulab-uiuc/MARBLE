# user.py
class User:
    def __init__(self, username, email, password):
        """
        Initialize a User object.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.email = email
        self.password = password
        self.stories = []

    def create_story(self, story_title):
        """
        Create a new story for the user.

        Args:
            story_title (str): The title of the story.
        """
        story = Story(story_title, self)
        self.stories.append(story)
        return story

    def edit_story(self, story_title, new_content):
        """
        Edit an existing story for the user.

        Args:
            story_title (str): The title of the story.
            new_content (str): The new content of the story.
        """
        for story in self.stories:
            if story.title == story_title:
                story.edit(new_content)
                return
        print("Story not found.")

    def delete_story(self, story_title):
        """
        Delete a story for the user.

        Args:
            story_title (str): The title of the story.
        """
        for story in self.stories:
            if story.title == story_title:
                self.stories.remove(story)
                return
        print("Story not found.")


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
        self.content = ""
        self.chapters = []
        self.versions = []
        self.comments = []
        self.ratings = []

    def add_chapter(self, chapter_title, chapter_content):
        """
        Add a new chapter to the story.

        Args:
            chapter_title (str): The title of the chapter.
            chapter_content (str): The content of the chapter.
        """
        chapter = Chapter(chapter_title, chapter_content)
        self.chapters.append(chapter)

    def edit(self, new_content):
        """
        Edit the content of the story.

        Args:
            new_content (str): The new content of the story.
        """
        self.content = new_content
        self.versions.append(self.content)

    def add_comment(self, comment):
        """
        Add a new comment to the story.

        Args:
            comment (str): The comment to add.
        """
        self.comments.append(comment)

    def add_rating(self, rating):
        """
        Add a new rating to the story.

        Args:
            rating (int): The rating to add.
        """
        self.ratings.append(rating)


# chapter.py
class Chapter:
    def __init__(self, title, content):
        """
        Initialize a Chapter object.

        Args:
            title (str): The title of the chapter.
            content (str): The content of the chapter.
        """
        self.title = title
        self.content = content


# collaborative_story_builder.py
class CollaborativeStoryBuilder:
    def __init__(self):
        """
        Initialize a CollaborativeStoryBuilder object.
        """
        self.users = []
        self.stories = []

    def register_user(self, username, email, password):def create_story(self, user, story_title):
    story = Story(story_title, user)
    self.stories.append(story)
    user.stories.append(story)
    return storydef login_user(self, username, password):
def add_comment(self, user, story_title, comment):def add_rating(self, user, story_title, rating):
    for story in self.stories:
        if story.title == story_title:
            story.add_rating(rating)
            return
    print("Story not found.")def add_rating(self, user, story_title, rating):
        for story in self.stories:
            if story.title == story_title and story.author == user:
                story.add_rating(rating)
                return
        print("You do not have permission to add a rating to this story.")
        for story in self.stories:
            if story.title == story_title and story.author == user:
                story.add_comment(comment)
                return
        print("You do not have permission to add a comment to this story.")def add_rating(self, user, story_title, rating):
        """
        Add a new rating to a story for a user.

        Args:
            user (User): The user who is adding the rating.
            story_title (str): The title of the story.
            rating (int): The rating to add.
        """
        for story in user.stories:
            if story.title == story_title:
                story.add_rating(rating)
                return
        print("Story not found.")


# main.py
def main():
    builder = CollaborativeStoryBuilder()

    user1 = builder.register_user("user1", "user1@example.com", "password1")
    user2 = builder.register_user("user2", "user2@example.com", "password2")

    story1 = builder.create_story(user1, "Story 1")
    story2 = builder.create_story(user2, "Story 2")

    builder.add_chapter(user1, "Story 1", "Chapter 1", "This is chapter 1.")
    builder.add_chapter(user2, "Story 2", "Chapter 1", "This is chapter 1.")

    builder.edit_story(user1, "Story 1", "This is the new content.")
    builder.edit_story(user2, "Story 2", "This is the new content.")

    builder.add_comment(user1, "Story 1", "This is a comment.")
    builder.add_comment(user2, "Story 2", "This is a comment.")

    builder.add_rating(user1, "Story 1", 5)
    builder.add_rating(user2, "Story 2", 5)

    builder.delete_story(user1, "Story 1")
    builder.delete_story(user2, "Story 2")


if __name__ == "__main__":
    main()