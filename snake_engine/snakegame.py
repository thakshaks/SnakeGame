import random

class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        # Starting snake coordinates
        self.snake = [
            {'x': 10, 'y': 10},
            {'x': 9, 'y': 10},
            {'x': 8, 'y': 10}
        ]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        self.food = self._spawn_food()

    def _spawn_food(self):
        while True:
            food = {
                'x': random.randint(0, self.width - 1),
                'y': random.randint(0, self.height - 1)
            }
            if food not in self.snake:
                return food

    def change_direction(self, new_dir):
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_dir in ['UP', 'DOWN', 'LEFT', 'RIGHT'] and new_dir != opposites.get(self.direction):
            self.next_direction = new_dir

    def update(self):
        if self.game_over:
            return self.get_state()

        self.direction = self.next_direction
        head = self.snake[0].copy()

        if self.direction == 'UP':
            head['y'] -= 1
        elif self.direction == 'DOWN':
            head['y'] += 1
        elif self.direction == 'LEFT':
            head['x'] -= 1
        elif self.direction == 'RIGHT':
            head['x'] += 1

        # Check Wall Collisions
        if head['x'] < 0 or head['x'] >= self.width or head['y'] < 0 or head['y'] >= self.height:
            self.game_over = True
            return self.get_state()

        # Check Self Collision
        if head in self.snake:
            self.game_over = True
            return self.get_state()

        # Advance Snake Head
        self.snake.insert(0, head)

        # Check Food Collision
        if head['x'] == self.food['x'] and head['y'] == self.food['y']:
            self.score += 10
            self.food = self._spawn_food()
        else:
            self.snake.pop()


        return self.get_state()

    
    def get_state(self):
        return {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'grid_size': {'width': self.width, 'height': self.height}
        }