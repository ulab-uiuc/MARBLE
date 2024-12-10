```python
import os
import time
import keyboard

# Game settings
WIDTH = 40
HEIGHT = 20
PADDLE_SIZE = 3
BALL_CHAR = '*'
PADDLE_CHAR = '|'
AI_SPEED = 0.1

# Initialize game variables
ball = {'x': WIDTH // 2, 'y': HEIGHT // 2, 'dx': 1, 'dy': 1}
player_paddle = HEIGHT // 2
ai_paddle = HEIGHT // 2

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_game():
    clear_screen()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == 0 or x == WIDTH - 1:
                print('#', end='')
            elif x == ball['x'] and y == ball['y']:
                print(BALL_CHAR, end='')
            elif x == 1 and player_paddle <= y < player_paddle + PADDLE_SIZE:
                print(PADDLE_CHAR, end='')
            elif x == WIDTH - 2 and ai_paddle <= y < ai_paddle + PADDLE_SIZE:
                print(PADDLE_CHAR, end='')
            else:
                print(' ', end='')
        print()

def update_ball_position():
    ball['x'] += ball['dx']
    ball['y'] += ball['dy']

    # Check for collisions with walls
    if ball['y'] == 0 or ball['y'] == HEIGHT - 1:
        ball['dy'] = -ball['dy']
    if ball['x'] == 2 and player_paddle <= ball['y'] < player_paddle + PADDLE_SIZE:
        ball['dx'] = -ball['dx']
    if ball['x'] == WIDTH - 3 and ai_paddle <= ball['y'] < ai_paddle + PADDLE_SIZE:
        ball['dx'] = -ball['dx']

def update_ai_paddle():
    if ball['y'] < ai_paddle + PADDLE_SIZE // 2:
        ai_paddle -= 1
    elif ball['y'] > ai_paddle + PADDLE_SIZE // 2:
        ai_paddle += 1

def main():
    while True:
        draw_game()
        update_ball_position()
        update_ai_paddle()

        if keyboard.is_pressed('up') and player_paddle > 1:
            player_paddle -= 1
        if keyboard.is_pressed('down') and player_paddle < HEIGHT - PADDLE_SIZE - 1:
            player_paddle += 1

        time.sleep(0.1)

if __name__ == '__main__':
    main()
```

The task description is: Build a basic ping pong game with simple AI opponent.
Based on this task description, I have improved the solution.