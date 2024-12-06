# Author: Lauren Kidman
# Date: 25 October 2024
# COSC 76: Artificial Intelligence 24F

import math
import random
import sys
import chess

class MinimaxAI():
    """
        Summary: Initializes the MinimaxAI class with the specified depth for search, sets up
            player, best move storage, and a node count tracker to count the visited nodes

        :param depth: the maximum depth to search in the minimax algorithm
    """
    def __init__(self, depth):
        self.depth = depth
        self.player = None
        self.best_move = None
        self.node_count = 0

    def cutoff_test(self, board, depth):
        """
        Summary: Determines if the search should be cut off due to reaching a terminal state (a win or a draw)
        or reaching the specified depth limit

        :param board: the ChessGame board
        :param depth: the current depth of the search
        :return: True if the search should stop, either because the depth is 0 or the game is over, otherwise False
        """
        return depth == 0 or board.is_game_over()

    # Run your minimax search
    def choose_move(self, board):
        """
        Summary: Executes the minimax search starting from depth 1 up to the specified maximum depth (utilizes IDS)

        :param board: the current board state
        :return: the best move, based on the minimax search up to the specified depth
        """
        # Following the pseudocode provided in the class textbook:
        self.node_count = 0
        self.player = board.turn

        for depth in range(1, self.depth+1, 1):
            value, move = self.max_value(board, depth)
            if move is not None:
                self.best_move = move

            print("Best move:", self.best_move)

        if board.is_game_over():
            print("Game Over:", board.outcome())
            sys.exit()
        else:
            print("MINIMAX Total nodes visited:", self.node_count)
            return self.best_move


    def evaluate(self, board):
        """
        Summary: Simple evaluation function that calculates the material advantage of the current player
        based on the number AND type of pieces on the board

        :param board: the current board state
        :return: a numeric score indicating the material advantage of the current player
        """
        # According to https://python-chess.readthedocs.io/en/latest/core.html -- chess class has piece types
        # We use a dictionary so we can store the value of each piece corresponding to its piece type
        piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                        chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100000}

        evaluation = 0
        for piece in piece_values:
            # We consider both the quality AND the quantity of each piece --
            # if you have more of one piece than your opponent, you are in a more favorable position
            if self.player:
                evaluation += len(board.pieces(piece, chess.WHITE)) * piece_values.get(piece)
                evaluation -= len(board.pieces(piece, chess.BLACK)) * piece_values.get(piece)
            else:
                evaluation -= len(board.pieces(piece, chess.WHITE)) * piece_values.get(piece)
                evaluation += len(board.pieces(piece, chess.BLACK)) * piece_values.get(piece)

        return evaluation

    def max_value(self, board, depth):
        """
        Summary: The maximizing function -- It simulates possible moves, evaluates the resulting board states,
        and recursively calls min_value to simulate the opponent's response

        :param board: the current board state
        :param depth: the current depth of the search
        :return: the highest value and corresponding move found for the maximizing player
        """
        self.node_count += 1

        if self.cutoff_test(board,depth):
            return self.evaluate(board), None

        v = -math.inf
        optimal_move = None

        moves = list(board.legal_moves)
        random.shuffle(moves)  # This makes sure its not repeating the same move multiple times (stalemate)

        for move in moves:
            board.push(move)
            v2, move2 = self.min_value(board, depth-1)

            if v2 > v:
                v, optimal_move = v2, move

            board.pop()

        return v, optimal_move

    def min_value(self, board, depth):
        """
        Summary: The minimizing function -- It simulates possible moves, evaluates the resulting board states,
        and recursively calls max_value to simulate the opponent's response

        :param board: the current board state
        :param depth: the current depth of the search
        :return: the lowest value and corresponding move found for the minimizing player
        """
        self.node_count += 1

        if self.cutoff_test(board, depth):
            return self.evaluate(board), None

        v = math.inf
        optimal_move = None

        moves = list(board.legal_moves)
        random.shuffle(moves)

        for move in moves:
            board.push(move)
            v2, move2 = self.max_value(board, depth - 1)

            if v2 < v:
                v, optimal_move = v2, move

            board.pop()

        return v, optimal_move
