# sports_team_collaborator.py

class SportsTeamCollaborator:
    def __init__(self):
        self.users = {}
        self.data = {}
        self.notes = {}
        self.comments = {}
        self.chat = {}

    def add_user(self, user_id, role):
        self.users[user_id] = role

    def upload_data(self, user_id, data_type, data):
        if user_id in self.users:
            if data_type in self.data:
                self.data[data_type].append(data)
            else:
                self.data[data_type] = [data]
        else:
            return "User not authorized to upload data."

    def add_note(self, user_id, note_id, note):
        if user_id in self.users:
            self.notes[note_id] = note
        else:
            return "User not authorized to add notes."

    def add_comment(self, user_id, comment_id, comment):
        if user_id in self.users:
            self.comments[comment_id] = comment
        else:
            return "User not authorized to add comments."

    def send_chat_message(self, user_id, message):
        if user_id in self.users:
            if "chat" in self.chat:
                self.chat["chat"].append(message)
            else:
                self.chat["chat"] = [message]
        else:
            return "User not authorized to send chat messages."

# Test cases
def test_sports_team_collaborator():
    stc = SportsTeamCollaborator()

    stc.add_user("coach1", "coach")
    stc.add_user("analyst1", "analyst")
    stc.add_user("player1", "player")

    assert stc.upload_data("coach1", "video", "video_file.mp4") is None
    assert stc.upload_data("analyst1", "csv", "performance_data.csv") is None
assert stc.upload_data("player1", "live", "live_data_stream") == "User not authorized to upload data."
    assert stc.upload_data("player2", "live", "live_data_stream") == "User not authorized to upload data."    stc.add_note("coach1", 1, "Note 1")

    assert stc.upload_data("player2", "live", "live_data_stream") == "User not authorized to upload data."
    stc.add_note("analyst1", 2, "Note 2")
    assert stc.notes == {1: "Note 1", 2: "Note 2"}

    stc.add_comment("coach1", 1, "Comment 1")
    stc.add_comment("analyst1", 2, "Comment 2")
    assert stc.comments == {1: "Comment 1", 2: "Comment 2"}

    stc.send_chat_message("coach1", "Hello from coach")
    stc.send_chat_message("analyst1", "Hello from analyst")
    assert stc.chat == {"chat": ["Hello from coach", "Hello from analyst"]}

    print("All test cases pass.")

if __name__ == "__main__":
    test_sports_team_collaborator()