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
        self.current_version = 0  # To track the current version index

    def upload_video(self, video_path):
        """Upload a video file to the project."""
        self.video_file = video_path
        print(f"Video uploaded: {video_path}")

    def upload_subtitle(self, subtitle_path):
        """Upload a subtitle file to the project and synchronize it."""
        self.subtitle_file = subtitle_path
        self.subtitles = self.auto_sync_subtitles(subtitle_path)
        print(f"Subtitle uploaded and synchronized: {subtitle_path}")def auto_sync_subtitles(self, subtitle_path):
        """Automatically synchronize subtitles with the video content, supporting multiple formats."""
        subtitles = []
        try:
            with open(subtitle_path, 'r') as file:
                if subtitle_path.endswith('.srt'):
                    for line in file:
                        if line.strip():
                            parts = line.split('-->')
                            if len(parts) == 2:
                                start_time = parts[0].strip()
                                text = parts[1].strip()
                                subtitles.append(f'[{start_time}] {text}')
                elif subtitle_path.endswith('.vtt'):
                    for line in file:
                        if line.startswith('00:'):
                            start_time = line.split(' ')[0]
                            text = next(file).strip()
                            subtitles.append(f'[{start_time}] {text}')
                else:
                    raise ValueError("Unsupported subtitle format. Please use SRT or VTT.")
            print("Subtitles synchronized.")
        except Exception as e:
            print(f"Error synchronizing subtitles: {e}")
        return subtitles    def adjust_playback_speed(self, speed):
        """Adjust the playback speed of the video."""
        if speed <= 0:
            raise ValueError("Playback speed must be greater than 0.")
        self.playback_speed = speed
        print(f"Playback speed adjusted to: {self.playback_speed}x")

    def send_chat_message(self, message):
        """Send a chat message to other users."""
        self.chat_messages.append(message)
        print(f"Chat message sent: {message}")

    def save_version(self):
        """Save the current version of the video project."""
        self.versions.append({
            'video_file': self.video_file,
            'subtitles': self.subtitles,
            'playback_speed': self.playback_speed,
            'chat_messages': self.chat_messages.copy()
        })
        self.current_version += 1
        print(f"Version {self.current_version} saved.")

    def revert_to_version(self, version_index):
        """Revert to a previous version of the video project."""
        if version_index < 0 or version_index >= len(self.versions):
            raise IndexError("Version index out of range.")
        version = self.versions[version_index]
        self.video_file = version['video_file']
        self.subtitles = version['subtitles']
        self.playback_speed = version['playback_speed']
        self.chat_messages = version['chat_messages']
        self.current_version = version_index
        print(f"Reverted to version {version_index}.")

    def display_chat(self):
        """Display all chat messages."""
        print("Chat messages:")
        for message in self.chat_messages:
            print(f"- {message}")

    def display_subtitles(self):
        """Display all synchronized subtitles."""
        print("Synchronized subtitles:")
        for subtitle in self.subtitles:
            print(subtitle)

# Example usage
if __name__ == "__main__":
    vcs = VideoCollaborationSuite()
    vcs.upload_video("example_video.mp4")
    vcs.upload_subtitle("example_subtitles.srt")
    vcs.adjust_playback_speed(1.5)
    vcs.send_chat_message("Let's start editing the video.")
    vcs.save_version()
    vcs.display_chat()
    vcs.display_subtitles()
    vcs.revert_to_version(0)