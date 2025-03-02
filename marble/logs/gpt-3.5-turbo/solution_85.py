# SportGame_Collaborative_Analytics

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Analyst(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.data = {}

    def input_data(self, player_name, score, assists):
        self.data[player_name] = {'score': score, 'assists': assists}

    def update_data(self, player_name, score=None, assists=None):
        if player_name in self.data:
            if score:
                self.data[player_name]['score'] = score
            if assists:
                self.data[player_name]['assists'] = assists

    def generate_report(self):
        report = "Player Performance Report:\n"
        for player, stats in self.data.items():
            report += f"Player: {player}, Score: {stats['score']}, Assists: {stats['assists']}\n"
        return report

class SportGameCollaborativeAnalytics:
    def __init__(self):
        self.analysts = {}

    def create_account(self, username, password):
        if username not in self.analysts:
            self.analysts[username] = Analyst(username, password)
            return True
        return False

    def authenticate(self, username, password):
        if username in self.analysts:
            return self.analysts[username].password == password
        return False

    def input_real_time_data(self, username, player_name, score, assists):
        if username in self.analysts:
            self.analysts[username].input_data(player_name, score, assists)
            return True
        return False

    def update_real_time_data(self, username, player_name, score=None, assists=None):
        if username in self.analysts:
            self.analysts[username].update_data(player_name, score, assists)
            return True
        return False

    def generate_report(self, username):
        if username in self.analysts:
            return self.analysts[username].generate_report()
        return "Analyst not found."

# Test cases
def run_tests():
    sport_analytics = SportGameCollaborativeAnalytics()

    # Test account creation and authentication
    assert sport_analytics.create_account("analyst1", "password1") == True
    assert sport_analytics.authenticate("analyst1", "password1") == True
    assert sport_analytics.authenticate("analyst1", "password2") == False

    # Test inputting real-time data
    assert sport_analytics.input_real_time_data("analyst1", "PlayerA", 10, 5) == True
    assert sport_analytics.input_real_time_data("analyst2", "PlayerB", 8, 3) == False

    # Test updating real-time data
    assert sport_analytics.update_real_time_data("analyst1", "PlayerA", score=15) == True
    assert sport_analytics.update_real_time_data("analyst2", "PlayerB", assists=4) == False

    # Test generating report
    report = sport_analytics.generate_report("analyst1")
    assert "PlayerA" in report
    assert "PlayerB" not in report

    print("All tests passed successfully.")

    # Test real-time collaboration
    assert sport_analytics.input_real_time_data("analyst1", "PlayerC", 12, 6) == True
    assert sport_analytics.input_real_time_data("analyst2", "PlayerD", 9, 4) == False
    assert sport_analytics.update_real_time_data("analyst1", "PlayerC", score=18) == True
    assert sport_analytics.update_real_time_data("analyst2", "PlayerD", assists=5) == False

if __name__ == "__main__":
    run_tests()