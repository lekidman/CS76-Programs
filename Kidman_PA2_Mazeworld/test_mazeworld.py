# Author: Lauren Kidman
# Date: 18 October 2024
# COSC 76: Artificial Intelligence 24F

from MazeworldProblem import MazeworldProblem
from Maze import Maze

from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


# Test problems

test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
#test_mp.animate_path(result.path)

# -------------------------------------------------
# Barrier-heavy maze
test_maze4 = Maze("maze4.maz")
test_mp4 = MazeworldProblem(test_maze4, (5,5,4,5,6,5))
result4 = astar_search(test_mp4, test_mp4.manhattan_heuristic)
print(result4)
#test_mp4.animate_path(result4.path)

# -------------------------------------------------
# A 40x40 maze with few barriers
test_maze5 = Maze("maze5.maz")
test_mp5 = MazeworldProblem(test_maze5, (38,22,5,31))
result5 = astar_search(test_mp5, test_mp5.manhattan_heuristic)
print(result5)
#test_mp5.animate_path(result5.path)

# -------------------------------------------------
# A tricky corridor maze
test_maze6 = Maze("maze6.maz")
test_mp6 = MazeworldProblem(test_maze6, (1,1,6,1,6,6))

result6 = astar_search(test_mp6, null_heuristic)
print(result6)
result6 = astar_search(test_mp6, test_mp6.manhattan_heuristic)
print(result6)
#test_mp6.animate_path(result6.path)

