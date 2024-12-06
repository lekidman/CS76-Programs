# Author: Lauren Kidman
# Date: 4 October 2024
# COSC 76: Artificial Intelligence 24F
from collections import deque
from SearchSolution import SearchSolution


class SearchNode:
    """
    Summary: Represents a node in a search tree or graph. Each node has a state and an optional parent
    (except for the root node)

    Attributes:
        state: The state represented by the node.
        parent: The parent node that led to this state. The root node will have no parent (None).
    """

    # Each search node except the root has a parent node
    # And all search nodes wrap a state object
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent


def backchain(search_node):
    """
        Summary: Constructs the path from the starting/root node to the given search node by
        traversing the parent pointers.

        :param search_node: The node from which the backchain process starts. This is typically the goal node
        after the search algorithm finds the solution.

        :return: A list of states representing the path from the starting/root node to the search_node (the goal).
        """
    path = []
    current_node = search_node
    path.append(current_node.state)

    while current_node.parent is not None:
        current_node = current_node.parent
        path.append(current_node.state)

    return path[::-1]  # Reverse it to go from beginning to end


def bfs_search(search_problem):
    """
    Summary: Performs a breadth-first search, utilizing memoization, on a given search problem

    :param search_problem: an object that contains a start state, a goal state, and a method to get successors
    from a given state

    :return: an object SearchSolution that contains the method of finding the solution, the path from the start state
    to the goal state, and the number of nodes visited
    """

    # Following the lecture 4 pseudocode:
    search_solution = SearchSolution(search_problem, "BFS")
    root = SearchNode(search_problem.start_state, None)

    frontier = deque([root])  # Fringe is a FIFO queue
    explored = set()  # Establish a set of visited nodes to ensure the same state is not explored more than once
    explored.add(root.state)

    while frontier:
        search_solution.nodes_visited += 1
        current_node = frontier.popleft()  # Use popleft since standard pop pulls from the last element of the list
        current_state = current_node.state

        # If the current node is our goal, we can stop building the frontier and return the path
        if search_problem.goal_test(current_state):
            # Use backchain to extract the goal path from the tree:
            search_solution.path = backchain(current_node)
            return search_solution

        # Otherwise, continue progressing through node children and building the frontier
        else:
            # Look through the next *level* of child states (as BFS)
            for child_state in search_problem.get_successors(current_state):
                # If the child has not already been visited, we add so it can be explored
                if child_state not in explored:
                    # Pack child state into a node, with backpointer to current_node
                    child_node = SearchNode(child_state, current_node)
                    frontier.append(child_node)
                    explored.add(current_state)

    return search_solution


# =====================================================================================

def dfs_search(search_problem, depth_limit=100, current_node=None, solution=None):
    """
        Summary: Performs a path-checking depth-first search on a given search problem

        :param search_problem: an object that contains a start state, a goal state, and a method to get successors
        from a given state

        :return: an object SearchSolution that contains the method of finding the solution, the path from the start state
        to the goal state, and the number of nodes visited
        """
    # Based on pseudocode from Lecture 4:
    # if no node object given, create a new search from starting state
    if current_node == None:
        current_node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    if depth_limit > 0:
        solution.nodes_visited += 1
        current_state = current_node.state

        if search_problem.goal_test(current_state):
            # Use backchain to extract the goal path from the tree:
            solution.path = backchain(current_node)
            return solution

        # Rather than an explored set, check if successors have been visited with backchain
        for child in search_problem.get_successors(current_state):
            if child not in backchain(current_node):
                child_node = SearchNode(child, current_node)
                next_solution = dfs_search(search_problem, depth_limit - 1, child_node, solution)

                if next_solution.path:
                    return next_solution  # if exists, call recursion with the child node as the
                    # new current node until solution is found

    # Return statement for if you go past the depth limit without finding a solution -- failure
    return solution


# =====================================================================================

def ids_search(search_problem, depth_limit=100):
    """
        Summary: Performs an iterative-deepening search on a given search problem

        :param search_problem: an object that contains a start state, a goal state, and a method to get successors
        from a given state

        :return: an object SearchSolution that contains the method of finding the solution, the path from the start state
        to the goal state, and the number of nodes visited
        """
    solution = SearchSolution(search_problem, "IDS")
    # try depth first search -- If no solution, increment limit by 1 and
    # start new search until depth limit is reached, after which failure

    for curr_depth in range(1, depth_limit + 1):
        iteration = dfs_search(search_problem, curr_depth)
        solution.nodes_visited += iteration.nodes_visited

        if iteration.path:
            solution.path = iteration.path
            return solution

    return solution
