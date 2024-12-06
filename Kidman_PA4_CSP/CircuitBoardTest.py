# Author: Lauren Kidman
# Date: 18 November 2024
# COSC 76: Artificial Intelligence 24F

import time
from CircuitBoardCSP import CircuitBoardCSP
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

# Initialize map and CSP solver objects:
small_board = CircuitBoardCSP(3, 3, [[2, 1], [1, 2]])
solver_small = ConstraintSatisfactionProblem(small_board)

# Define usage booleans for heuristics + inference:
use_mrv = False
use_lcv = False
use_degree = False
use_ac3 = False

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver_small.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("Small Board without heuristics/inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(small_board.format_nums_to_text(solution))
    print("States visited: ", solver_small.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

medium_board = CircuitBoardCSP(10, 3, [[3, 2], [5, 2], [2, 3], [7, 1]])
solver_medium = ConstraintSatisfactionProblem(medium_board)

# Define usage booleans for heuristics + inference:
use_mrv = False
use_lcv = False
use_degree = False
use_ac3 = False

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver_medium.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nMedium Board without heuristics/inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(medium_board.format_nums_to_text(solution))
    print("States visited: ", solver_medium.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

large_board = CircuitBoardCSP(8, 8, [
    [4, 4],
    [2, 6],
    [6, 2],
    [2, 2],
    [3, 1],
])
solver_large = ConstraintSatisfactionProblem(large_board)

# Define usage booleans for heuristics + inference:
use_mrv = False
use_lcv = False
use_degree = False
use_ac3 = False

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver_large.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nLarge Board without heuristics/inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(large_board.format_nums_to_text(solution))
    print("No heuristics/inference -- states visited: ", solver_large.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

# Redefine usage booleans for heuristics + inference for large board to compare:
use_mrv = True
use_lcv = True
use_degree = True
use_ac3 = True

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver_large.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nLarge Board with all heuristics/inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(large_board.format_nums_to_text(solution))
    print("With all heuristics/inference -- states visited: ", solver_large.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

huge_components = [
    [3, 4], [5, 2], [2, 6], [7, 3], [4, 5], [6, 4], [2, 2], [8, 1],
    [3, 3], [5, 5], [4, 2], [6, 3], [1, 7], [2, 4], [7, 2], [3, 6],
    [5, 3], [4, 4], [2, 3], [6, 2], [3, 1], [5, 6], [4, 1], [8, 2]
]

huge_board = CircuitBoardCSP(20, 20, huge_components)
solver_huge = ConstraintSatisfactionProblem(huge_board)

# Define usage booleans for heuristics + inference:
use_mrv = False
use_lcv = False
use_degree = False
use_ac3 = False

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver_huge.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nHuge Board without heuristics/inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(huge_board.format_nums_to_text(solution))
    print("No heuristics/inference -- states visited: ", solver_huge.get_states_visited())
    #print("No heuristics/inference -- backtracks: ", solver_huge.get_backtrack_count())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

# Define usage booleans for heuristics + inference:
use_mrv = True
use_lcv = True
use_degree = True
use_ac3 = True

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver_huge.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nHuge Board with all heuristics/inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(huge_board.format_nums_to_text(solution))
    print("With all heuristics/inference -- states visited: ", solver_huge.get_states_visited())
    #print("With all heuristics/inference -- backtracks: ", solver_huge.get_backtrack_count())
else:
    print("No solution found.")