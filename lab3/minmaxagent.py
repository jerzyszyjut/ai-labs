from exceptions import AgentException
from copy import deepcopy


class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token
        self.win_patterns = [
            [(0, 1), (0, 2), (0, 3)],
            [(1, 0), (2, 0), (3, 0)],
            [(1, 1), (2, 2), (3, 3)],
            [(1, -1), (2, -2), (3, -3)]
        ]

    def evaluate_board(self, board, current_player):
        my_score = 0
        other_score = 0

        for player in ['o', 'x']:
            for pattern in self.win_patterns:
                for row in range(board.height):
                    for col in range(board.width):
                        score = self.check_pattern(board, player, pattern, row, col)
                        if player == self.my_token:
                            my_score = max(my_score, score)
                        else:
                            other_score = max(other_score, score)

        if current_player == self.my_token:
            return my_score - other_score
        else:
            return other_score - my_score

    def check_pattern(self, board, player, pattern, row, col):
        score = 0
        for dr, dc in pattern:
            total = 0
            for i in range(4):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < board.height and 0 <= c < board.width:
                    if board.board[r][c] == player:
                        total += 1
                    elif board.board[r][c] != '_':
                        total = 0
                        break
                else:
                    total = 0
                    break
            score = max(score, total / 4)
        return score

    def other_player(self, player):
        return 'o' if player == 'x' else 'x'

    def minmax(self, board, current_player, depth):
        if board.game_over:
            if board.wins == self.my_token:
                return 1
            elif board.wins is not None:
                return -1
            return 0
    
        if depth == 0:
            return self.evaluate_board(board, current_player)

        if current_player == self.my_token:
            maximum = -float('inf')
            for column in board.possible_drops():
                new_board = deepcopy(board)
                new_board.drop_token(column)
                value = self.minmax(new_board, self.other_player(current_player), depth-1)
                maximum = max(maximum, value)
            return maximum
        else:
            minimum = float('inf')
            for column in board.possible_drops():
                new_board = deepcopy(board)
                new_board.drop_token(column)
                value = self.minmax(new_board, self.other_player(current_player), depth-1)
                minimum = min(minimum, value)
            return minimum
        
    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        maximum = -float('inf')
        best_column = None
        for column in connect4.possible_drops():
            new_board = deepcopy(connect4)
            new_board.drop_token(column)
            value = self.minmax(new_board, self.other_player(self.my_token), 2)
            if value > maximum:
                maximum = value
                best_column = column
        return best_column
    