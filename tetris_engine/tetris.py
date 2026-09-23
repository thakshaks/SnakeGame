import random

SHAPES = [
    [[1, 1, 1, 1]],                              # I
    [[1, 1], [1, 1]],                            # O
    [[0, 1, 0], [1, 1, 1]],                      # T
    [[1, 0, 0], [1, 1, 1]],                      # L
    [[0, 0, 1], [1, 1, 1]],                      # J
    [[0, 1, 1], [1, 1, 0]],                      # S
    [[1, 1, 0], [0, 1, 1]]                       # Z
]

class TetrisGame:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.game_over = False
        self.current_piece = self._new_piece()
        self.piece_x = self.width // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        return self.get_state()

    def _new_piece(self):
        return random.choice(SHAPES)

    def _check_collision(self, piece, offset_x, offset_y):
        for y, row in enumerate(piece):
            for x, val in enumerate(row):
                if val:
                    new_x = offset_x + x
                    new_y = offset_y + y
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False

    def handle_input(self, action):
        if self.game_over:
            return

        if action == 'LEFT':
            if not self._check_collision(self.current_piece, self.piece_x - 1, self.piece_y):
                self.piece_x -= 1
        elif action == 'RIGHT':
            if not self._check_collision(self.current_piece, self.piece_x + 1, self.piece_y):
                self.piece_x += 1
        elif action == 'DOWN':
            if not self._check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
                self.piece_y += 1
        elif action == 'ROTATE':
            # Transpose and reverse rows for 90-degree rotation
            rotated = [list(row) for row in zip(*self.current_piece[::-1])]
            if not self._check_collision(rotated, self.piece_x, self.piece_y):
                self.current_piece = rotated

    def update(self):
        if self.game_over:
            return self.get_state()

        # Step downward
        if not self._check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            # Lock piece into board
            for y, row in enumerate(self.current_piece):
                for x, val in enumerate(row):
                    if val:
                        board_y = self.piece_y + y
                        board_x = self.piece_x + x
                        if board_y < 0:
                            self.game_over = True
                            return self.get_state()
                        self.board[board_y][board_x] = 1

            # Clear full rows
            new_board = [row for row in self.board if not all(row)]
            rows_cleared = self.height - len(new_board)
            if rows_cleared > 0:
                self.score += rows_cleared * 100
                for _ in range(rows_cleared):
                    new_board.insert(0, [0 for _ in range(self.width)])
                self.board = new_board

            # Spawn next piece
            self.current_piece = self._new_piece()
            self.piece_x = self.width // 2 - len(self.current_piece[0]) // 2
            self.piece_y = 0

            if self._check_collision(self.current_piece, self.piece_x, self.piece_y):
                self.game_over = True

        return self.get_state()

    def get_state(self):
        return {
            'board': self.board,
            'current_piece': self.current_piece,
            'piece_x': self.piece_x,
            'piece_y': self.piece_y,
            'score': self.score,
            'game_over': self.game_over
        }