from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent
from alphabetaagent import AlphaBetaAgent

GAMES_COUNT = 10

agent1_wins = 0
agent2_wins = 0
for i in range(GAMES_COUNT):
    connect4 = Connect4(width=7, height=6, randomize=True)
    agent1 = AlphaBetaAgent('o', depth=4)
    agent2 = MinMaxAgent('x', depth=2)
    while not connect4.game_over:
        connect4.draw()
        try:
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(connect4)
            else:
                n_column = agent2.decide(connect4)
            connect4.drop_token(n_column)
        except (ValueError, GameplayException):
            print('invalid move')
        print("Game no:", i+1)
    
    if connect4.wins == agent1.my_token:
        agent1_wins += 1
    elif connect4.wins == agent2.my_token:
        agent2_wins += 1

print('agent1 wins:', agent1_wins)
print('agent2 wins:', agent2_wins)
print('ties:', GAMES_COUNT - agent1_wins - agent2_wins)
