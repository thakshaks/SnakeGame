# games/snake.py
import random

class SnakeGame:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.snake = [[10, 10], [10, 11], [10, 12]]
        self.direction = "UP"
        self.food = [5, 5]
        self.game_over = False
        self.score = 0

    def handle_input(self, action_data):
        new_dir = action_data.get('direction')
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if opposites.get(new_dir) != self.direction:
            self.direction = new_dir

    def tick(self):
        if self.game_over:
            return

        head = self.snake[0].copy()
        if self.direction == "UP": head[1] -= 1
        elif self.direction == "DOWN": head[1] += 1
        elif self.direction == "LEFT": head[0] -= 1
        elif self.direction == "RIGHT": head[0] += 1

        # Check collisions
        if head[0] < 0 or head[0] >= self.grid_size or head[1] < 0 or head[1] >= self.grid_size or head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.score += 1
            while True:
                new_food = [random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)]
                if new_food not in self.snake:
                    self.food = new_food
                    break
        else:
            self.snake.pop()

    def get_state(self):
        # Returns JSON-serializable data for the frontend
        return {
            "game_type": "snake",
            "snake": self.snake,
            "food": self.food,
            "game_over": self.game_over,
            "score": self.score
        }