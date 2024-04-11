from exceptions import AgentException
from copy import deepcopy


class MinMaxAgent:
    def __init__(self, my_token='o', depth=2, heuristic=True):
        self.my_token = my_token
        self.win_patterns = [
            [(0, 1), (0, 2), (0, 3)],
            [(1, 0), (2, 0), (3, 0)],
            [(1, 1), (2, 2), (3, 3)],
            [(1, -1), (2, -2), (3, -3)]
        ]
        self.depth = depth
        self.heuristic = heuristic

    def evaluate_board(self, board, current_player):
        my_score = 0
        other_score = 0

        for player in ['o', 'x']:
            flag = False
            for pattern in self.win_patterns:
                if flag:
                    break
                for row in range(board.height):
                    if flag:
                        break
                    for col in range(board.width):
                        score = self.check_pattern(board, player, pattern, row, col)
                        if player == self.my_token:
                            my_score = max(my_score, score)
                        else:
                            other_score = max(other_score, score)
                        if player == self.my_token and my_score == 1:
                            flag = True
                            break
                        if player != self.my_token and other_score == 1:
                            flag = True
                            break

        if current_player == self.my_token and my_score == 1:
            return 1
        
        if current_player != self.my_token and other_score == 1:
            return -1
        
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
                        total = max(total, 0)
                        break
                else:
                    total = max(total, 0)
                    break
            if total == 3:
                score += total / 8
                score = min(total, 7 / 8)
            else:
                score = max(score, total / 8)
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
    
        if depth == 0 and self.heuristic:
            return self.evaluate_board(board, current_player)
        if depth == 0 and not self.heuristic:
            return 0

        if current_player == self.my_token:
            value = -float('inf')
            value_function = max
        else:
            value = float('inf')
            value_function = min

        for column in board.possible_drops():
            new_board = deepcopy(board)
            new_board.drop_token(column)
            value = value_function(self.minmax(new_board, self.other_player(current_player), depth-1), value)
        return value
        
    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        value = -float('inf')
        best_column = None
        for column in connect4.possible_drops():
            new_board = deepcopy(connect4)
            new_board.drop_token(column)
            new_value = self.minmax(new_board, self.other_player(self.my_token), self.depth)
            if new_value > value:
                value = new_value
                best_column = column
        return best_column
    