# Author: Lauren Kidman
# Date: 18 November 2024
# COSC 76: Artificial Intelligence 24F

import time
from AustralianMapCSP import AustralianMapCSP
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

# Initialize map and CSP solver objects:
australian_map = AustralianMapCSP()
solver = ConstraintSatisfactionProblem(australian_map)

# Define usage booleans for heuristics + inference:
use_mrv = False
use_lcv = False
use_degree = False
use_ac3 = False

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("No Heuristics or Inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(australian_map.format_nums_to_text(solution))
    print("States visited: ", solver.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

# Define usage booleans for heuristics + inference:
use_mrv = True
use_lcv = True
use_degree = True
use_ac3 = True
solver.states_visited = 0  # Reset the counter

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nAll Heuristics and Inference: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(australian_map.format_nums_to_text(solution))
    print("States visited: ", solver.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

# Define usage booleans for heuristics + inference:
use_mrv = False
use_lcv = False
use_degree = False
use_ac3 = True
solver.states_visited = 0  # Reset the counter

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nHeuristics False, Inference True: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(australian_map.format_nums_to_text(solution))
    print("States visited: ", solver.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

# Define usage booleans for heuristics + inference:
use_mrv = True
use_lcv = True
use_degree = True
use_ac3 = False
solver.states_visited = 0  # Reset the counter

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nHeuristics True, Inference False: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(australian_map.format_nums_to_text(solution))
    print("States visited: ", solver.get_states_visited())
else:
    print("No solution found.")

# -----------------------------------------------------------------------------

# Define usage booleans for heuristics + inference:
use_mrv = True
use_lcv = False
use_degree = True
use_ac3 = False
solver.states_visited = 0  # Reset the counter

# Call the backtracking search method with the applied settings and measure time:
start_time = time.time()
solution = solver.backtracking_search(use_mrv, use_lcv, use_degree, use_ac3)
end_time = time.time()
print("\n\nMRV + Degree Heuristics True, LCV + Inference False: {:.4f} seconds".format(end_time - start_time))

# Check if a solution was found and print results:
if solution is not None:
    print(australian_map.format_nums_to_text(solution))
    print("States visited: ", solver.get_states_visited())
else:
    print("No solution found.")