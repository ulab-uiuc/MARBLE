import unittest
from snake_game import SnakeGame

class TestSnakeGame(unittest.TestCase):
    def test_initialization(self):
        game = SnakeGame()
        self.assertEqual(game.score, 0)
        self.assertEqual(len(game.snake), 1)
        self.assertEqual(game.snake[0], (0, 0))
        self.assertEqual(game.food, None)

if __name__ == '__main__':
    unittest.main()