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
            value = -float('inf')
            for column in board.possible_drops():
                new_board = deepcopy(board)
                new_board.drop_token(column)
                value = max(value, self.minmax(new_board, self.other_player(current_player), depth-1, alpha, beta))
                alpha = max(alpha, value)
                if value >= beta:
                    break
            return value
        else:
            value = float('inf')
            for column in board.possible_drops():
                new_board = deepcopy(board)
                new_board.drop_token(column)
                value = min(value, self.minmax(new_board, self.other_player(current_player), depth-1, alpha, beta))
                beta = min(beta, value)
                if value <= alpha:
                    break
            return value

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        alpha = -float('inf')
        value = -float('inf')
        best_column = None
        for column in connect4.possible_drops():
            new_board = deepcopy(connect4)
            new_board.drop_token(column)
            new_value = self.minmax(new_board, self.other_player(self.my_token), self.depth)
            if new_value > value:
                value = new_value
                best_column = column
                alpha = max(alpha, value)
        return best_column