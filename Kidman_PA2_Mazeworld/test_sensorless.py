# You write this: (following the structure of test_mazeworld.py)
from SensorlessProblem import SensorlessProblem
from Maze import Maze

from astar_search import astar_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


# Test problems

test_maze3 = Maze("maze3.maz")
test_mp = SensorlessProblem(test_maze3, (1, 2))

print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# this should do a bit better:
result = astar_search(test_mp, test_mp.h1_min_manhattan)
print(result)

# test_mp.animate_path(result.path)

# -------------------------------------------------
# Small maze
test_maze7 = Maze("maze7.maz")
test_mp7 = SensorlessProblem(test_maze7, (0, 1))

result7 = astar_search(test_mp7, null_heuristic)
print(result7)
result7 = astar_search(test_mp7, test_mp7.h1_min_manhattan)
print(result7)
test_mp7.animate_path(result7.path)

# -------------------------------------------------
# Barrier-heavy maze
test_maze8 = Maze("maze8.maz")
test_mp8 = SensorlessProblem(test_maze8, (1, 4))

result8 = astar_search(test_mp8, null_heuristic)
print(result8)
result8 = astar_search(test_mp8, test_mp8.h1_min_manhattan)
print(result8)
test_mp8.animate_path(result8.path)
