from exceptions import AgentException
from copy import deepcopy
from minmaxagent import MinMaxAgent

class AlphaBetaAgent(MinMaxAgent):
    def minmax(self, board, current_player, depth, alpha=-float('inf'), beta=float('inf')):
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
                value = self.minmax(new_board, self.other_player(current_player), depth-1, alpha, beta)
                maximum = max(maximum, value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return maximum
        else:
            minimum = float('inf')
            for column in board.possible_drops():
                new_board = deepcopy(board)
                new_board.drop_token(column)
                value = self.minmax(new_board, self.other_player(current_player), depth-1, alpha, beta)
                minimum = min(minimum, value)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return minimum

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        maximum = -float('inf')
        best_column = None
        for column in connect4.possible_drops():
            new_board = deepcopy(connect4)
            new_board.drop_token(column)
            value = self.minmax(new_board, self.other_player(self.my_token), 3)
            if value > maximum:
                maximum = value
                best_column = column
        return best_column