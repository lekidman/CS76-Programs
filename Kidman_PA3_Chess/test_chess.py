# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys


player1 = MinimaxAI(2)
player2 = RandomAI()

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()

print("Game over! Game outcome: ", game.board.outcome())
#print(hash(str(game.board)))
