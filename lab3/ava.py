from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent
from alphabetaagent import AlphaBetaAgent

agent1_wins = 0
agent2_wins = 0
for i in range(5):
    connect4 = Connect4(width=7, height=6)
    agent1 = AlphaBetaAgent('o')
    agent2 = MinMaxAgent('x')
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
