# Author: Lauren Kidman
# Date: 25 October 2024
# COSC 76: Artificial Intelligence 24F

import math
import random
import sys
#from time import sleep
import chess
import math


class AlphaBetaAI:
    """
    Summary: Implements the Alpha-Beta Pruning algorithm, an enhanced version of the Minimax algorithm,
    by eliminating unnecessary branches to improve efficiency (and still giving the same optimal moves)

    :param depth: The maximum search depth for Alpha-Beta pruning
    """
    def __init__(self, depth):
        self.depth = depth
        self.player = None
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

    def choose_move(self, board):
        """
        Summary: Executes the Alpha-Beta search algorithm to choose the best move, starts by initializing alpha to
        negative infinity and beta to positive infinity

        :param board: The current chess board state
        :return: The optimal move based on the Alpha-Beta pruning algorithm
        """
        # Following the pseudocode provided in the class textbook:
        self.node_count = 0
        self.player = board.turn

        value, move = self.max_value(board, self.depth, -math.inf, math.inf)

        if board.is_game_over():
            print("Game Over:", board.outcome())
            sys.exit()
        else:
            print("ALPHABETA Total nodes visited:", self.node_count)
            return move

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

    def max_value(self, board, depth, alpha, beta):
        """
        Summary: The maximizing player evaluates the board to maximize the evaluation score --
        Alpha-Beta pruning is applied to avoid evaluating unnecessary branches (when a better move
        has already been found)

        :param board: The current chess board state
        :param depth: The current depth of the search
        :param alpha: The best value that the maximizing player has found so far
        :param beta: The best value that the minimizing player has found so far
        :return: The highest value and the corresponding move found for the maximizing player
        """
        self.node_count += 1

        if self.cutoff_test(board, depth):
            return self.evaluate(board), None

        v = -math.inf  # v represents utility
        optimal_move = None

        moves = list(board.legal_moves)
        random.shuffle(moves)  # This makes sure its not repeating the same move multiple times (stalemate)

        for move in moves:
            board.push(move)  # Make the move
            v2, move2 = self.min_value(board, depth - 1, alpha, beta)

            if v2 > v:
                v, optimal_move = v2, move
                alpha = max(alpha, v)

            board.pop()  # Undo the move for memory purposes

            if v >= beta:  # Beta cutoff, so no need to explore further
                return v, optimal_move

        return v, optimal_move

    def min_value(self, board, depth, alpha, beta):
        """
        Summary: The minimizing player evaluates the board to minimize the evaluation score --
        Alpha-Beta pruning is applied to avoid evaluating unnecessary branches (when a better move
        has already been found)

        :param board: The current chess board state
        :param depth: The current depth of the search
        :param alpha: The best value that the maximizing player has found so far
        :param beta: The best value that the minimizing player has found so far
        :return: The lowest value and the corresponding move found for the minimizing player
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
            v2, move2 = self.max_value(board, depth - 1, alpha, beta)

            if v2 < v:
                v, optimal_move = v2, move
                beta = min(beta, v)

            board.pop()

            if v <= alpha:
                return v, optimal_move

        return v, optimal_move
