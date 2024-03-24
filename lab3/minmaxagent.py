from exceptions import AgentException
from copy import deepcopy


class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def evaluate_board(self, board, player):
        score = 0

        for row in range(board.height):
            for column in range(board.width-3):
                if board.board[row][column] == board.board[row][column+1] == player and board.board[row][column+2] == board.board[row][column+3] == '_':
                    score = max(score, 0.4)
                if board.board[row][column] == board.board[row][column+1] == board.board[row][column+2] == player and board.board[row][column+3] == '_':
                    score = max(score, 0.8)
                if board.board[row][column] == board.board[row][column+1] == board.board[row][column+2] == board.board[row][column+3] == player:
                    score = max(score, 1)

        for row in range(board.height-3):
            for column in range(board.width):
                if board.board[row][column] == board.board[row+1][column] == player and board.board[row+2][column] == board.board[row+3][column] == '_':
                    score = max(score, 0.4)
                if board.board[row][column] == board.board[row+1][column] == board.board[row+2][column] == player and board.board[row+3][column] == '_':
                    score = max(score, 0.8)
                if board.board[row][column] == board.board[row+1][column] == board.board[row+2][column] == board.board[row+3][column] == player:
                    score = max(score, 1)

        for row in range(board.height-3):
            for column in range(board.width-3):
                if board.board[row][column] == board.board[row+1][column+1] == player and board.board[row+2][column+2] == board.board[row+3][column+3] == '_':
                    score = max(score, 0.4)
                if board.board[row][column] == board.board[row+1][column+1] == board.board[row+2][column+2] == player and board.board[row+3][column+3] == '_':
                    score = max(score, 0.8)
                if board.board[row][column] == board.board[row+1][column+1] == board.board[row+2][column+2] == board.board[row+3][column+3] == player:
                    score = max(score, 1)

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
            return self.evaluate_board(board, self.my_token) - self.evaluate_board(board, self.other_player(self.my_token))

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
            value = self.minmax(new_board, self.other_player(self.my_token), 4)
            if value > maximum:
                maximum = value
                best_column = column
        return best_column
    