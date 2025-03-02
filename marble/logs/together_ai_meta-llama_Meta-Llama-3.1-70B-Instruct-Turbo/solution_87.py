# solution.py

# models.py
class User:
    """Represents a user in the system."""
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

class Video:
    """Represents a video in the system."""
    def __init__(self, id, title, file):
        self.id = id
        self.title = title
        self.file = file

class PerformanceMetric:
    """Represents a performance metric in the system."""
    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value

class Message:
    """Represents a message in the system."""
    def __init__(self, id, text, sender):
        self.id = id
        self.text = text
        self.sender = sender

# services.py
class UserService:
    """Provides user-related functionality."""
    def __init__(self):
        self.users = []

    def add_user(self, user):
        """Adds a user to the system."""
        self.users.append(user)

    def get_user(self, id):
        """Gets a user by ID."""
        for user in self.users:
            if user.id == id:
                return user
        return None

class VideoService:
    """Provides video-related functionality."""
    def __init__(self):
        self.videos = []

    def add_video(self, video):
        """Adds a video to the system."""
        self.videos.append(video)

    def get_video(self, id):
        """Gets a video by ID."""
        for video in self.videos:
            if video.id == id:
                return video
        return None

    def analyze_video(self, video):
        """Analyzes a video and returns performance metrics."""
        # Simulate video analysis
        metrics = [
            PerformanceMetric(1, "Speed", 10),
            PerformanceMetric(2, "Accuracy", 20),
            PerformanceMetric(3, "Agility", 30)
        ]
        return metrics

class PerformanceService:
    """Provides performance-related functionality."""
    def __init__(self):
        self.metrics = []

    def add_metric(self, metric):
        """Adds a performance metric to the system."""
        self.metrics.append(metric)

    def get_metrics(self):
        """Gets all performance metrics."""
        return self.metrics

class MessageService:
    """Provides message-related functionality."""
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        """Adds a message to the system."""
        self.messages.append(message)

    def get_messages(self):
        """Gets all messages."""
        return self.messages

# controllers.py
class UserController:
    """Provides user-related functionality."""
    def __init__(self, user_service):
        self.user_service = user_service

    def register(self, username, role):
        """Registers a new user."""
        user = User(len(self.user_service.users) + 1, username, role)
        self.user_service.add_user(user)
        return user

    def login(self, username, role):
        """Logs in a user."""
        for user in self.user_service.users:
            if user.username == username and user.role == role:
                return user
        return None

class VideoController:
    """Provides video-related functionality."""
    def __init__(self, video_service, performance_service):
        self.video_service = video_service
        self.performance_service = performance_service

    def upload_video(self, title, file):
        """Uploads a video."""
        video = Video(len(self.video_service.videos) + 1, title, file)
        self.video_service.add_video(video)
        return video

    def analyze_video(self, video_id):
        """Analyzes a video."""
        video = self.video_service.get_video(video_id)
        if video:
            metrics = self.video_service.analyze_video(video)
            for metric in metrics:
                self.performance_service.add_metric(metric)
            return metrics
        return None

class PerformanceController:
    """Provides performance-related functionality."""
    def __init__(self, performance_service):
        self.performance_service = performance_service

    def get_performance(self):
        """Gets performance metrics."""
        return self.performance_service.get_metrics()

class MessageController:
    """Provides message-related functionality."""
    def __init__(self, message_service):
        self.message_service = message_service

    def send_message(self, text, sender):
        """Sends a message."""
        message = Message(len(self.message_service.messages) + 1, text, sender)
        self.message_service.add_message(message)
        return message

    def get_messages(self):
        """Gets messages."""
        return self.message_service.get_messages()

# main.py
def main():
    # Initialize services
    user_service = UserService()
    video_service = VideoService()
    performance_service = PerformanceService()
    message_service = MessageService()

    # Initialize controllers
    user_controller = UserController(user_service)
    video_controller = VideoController(video_service, performance_service)
    performance_controller = PerformanceController(performance_service)
    message_controller = MessageController(message_service)

    # Register users
    coach = user_controller.register("Coach", "Coach")
    player = user_controller.register("Player", "Player")
    analyst = user_controller.register("Analyst", "Analyst")

    # Upload video
    video = video_controller.upload_video("Game 1", "game1.mp4")

    # Analyze video
    metrics = video_controller.analyze_video(video.id)

    # Get performance metrics
    performance = performance_controller.get_performance()

    # Send messages
    message_controller.send_message("Hello, team!", coach)
    message_controller.send_message("Let's win this game!", player)

    # Get messages
    messages = message_controller.get_messages()

    # Print results
    print("Users:")
    print(coach.username, coach.role)
    print(player.username, player.role)
    print(analyst.username, analyst.role)

    print("\nVideo:")
    print(video.title, video.file)

    print("\nPerformance Metrics:")
    for metric in metrics:
        print(metric.name, metric.value)

    print("\nMessages:")
    for message in messages:
        print(message.text, message.sender.username)

if __name__ == "__main__":
    main()