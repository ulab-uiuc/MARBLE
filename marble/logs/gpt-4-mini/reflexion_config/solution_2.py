# solution.py

class VideoCollaborationSuite:
    def __init__(self):
        # Initialize the video project with empty attributes
        self.video_file = None
        self.subtitle_file = None
        self.subtitles = []
        self.playback_speed = 1.0  # Normal speed
        self.chat_messages = []
        self.versions = []  # To keep track of different versions of the video
        self.current_version_index = -1  # No version selected initially

    def upload_video(self, video_file):
        """Upload a video file to the project."""
        self.video_file = video_file
        print(f"Video '{video_file}' uploaded.")

    def upload_subtitle(self, subtitle_file):
        """Upload a subtitle file and synchronize it with the video."""
        self.subtitle_file = subtitle_file
        self.subtitles = self.auto_sync_subtitles(subtitle_file)
        print(f"Subtitle '{subtitle_file}' uploaded and synchronized.")import pysrt

    def auto_sync_subtitles(self, subtitle_file):
        """Automatically synchronize subtitles with the video content."""
        print(f"Synchronizing subtitles from '{subtitle_file}'...")
        subs = pysrt.open(subtitle_file)
        synchronized_subs = []
        for sub in subs:
            synchronized_subs.append(f'[{sub.start.to_time()}] {sub.text}')
        return synchronized_subs    def adjust_playback_speed(self, speed):
        """Adjust the playback speed of the video."""
        if speed <= 0:
            raise ValueError("Playback speed must be greater than 0.")
        self.playback_speed = speed
        print(f"Playback speed adjusted to {self.playback_speed}x.")

    def add_chat_message(self, user, message):
        """Add a chat message to the chat log."""
        self.chat_messages.append(f"{user}: {message}")
        print(f"Chat message added: {user}: {message}")

    def save_version(self):
        """Save the current version of the video project."""
        self.versions.append({
            'video_file': self.video_file,
            'subtitles': self.subtitles,
            'playback_speed': self.playback_speed,
            'chat_messages': self.chat_messages.copy()
        })
        self.current_version_index += 1
        print(f"Version {self.current_version_index + 1} saved.")

    def revert_to_version(self, version_index):
        """Revert to a previous version of the video project."""
        if version_index < 0 or version_index >= len(self.versions):
            raise IndexError("Version index out of range.")
        version = self.versions[version_index]
        self.video_file = version['video_file']
        self.subtitles = version['subtitles']
        self.playback_speed = version['playback_speed']
        self.chat_messages = version['chat_messages']
        self.current_version_index = version_index
        print(f"Reverted to version {version_index + 1}.")

    def display_chat(self):
        """Display the chat messages."""
        print("Chat Messages:")
        for message in self.chat_messages:
            print(message)

    def display_subtitles(self):
        """Display the synchronized subtitles."""
        print("Subtitles:")
        for subtitle in self.subtitles:
            print(subtitle)

# Example usage
if __name__ == "__main__":
    vcs = VideoCollaborationSuite()
    vcs.upload_video("example_video.mp4")
    vcs.upload_subtitle("example_subtitles.srt")
    vcs.adjust_playback_speed(1.5)
    vcs.add_chat_message("User1", "Let's sync the subtitles.")
    vcs.save_version()
    vcs.display_chat()
    vcs.display_subtitles()
    vcs.revert_to_version(0)  # Revert to the first version