# Author: Lauren Kidman
# Date: 18 October 2024
# COSC 76: Artificial Intelligence 24F
from SearchSolution import SearchSolution
from heapq import heappush, heappop


class AstarNode:
    """
    Summary: Represents a node in the A* search algorithm

    Attributes:
        state: The state of the search node
        heuristic: The heuristic value of the state
        parent: The parent node of the current node, used for backtracking the path
        cost: The total cost to reach this node from the start node, including transition costs
        """
    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.cost = transition_cost

    def priority(self):
        """
        Summary: Priority is determined by the value of cost + heuristic

        :return: priority value, equals heuristic + cost
        """
        return self.heuristic + self.cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


#  Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    """
    Summary: Take the current node, and follow its parents back as far as possible

    :param node: the current node
    :return: the list of states up until the current state
    """
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    """
    Summary: Performs A* search on the given search problem using the specified heuristic function

    :param search_problem: An instance of the MazeworldProblem containing the maze and the goal locations
    :param heuristic_fn: A function that computes the heuristic value for a given state, which guides the search
    :return: An instance of SearchSolution containing the path to the goal, total cost, and number of nodes visited
    """
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:
    while pqueue:
        current_node = heappop(pqueue)
        current_state = current_node.state

        solution.nodes_visited += 1

        # Like with other search algorithms, first check if the current state is the goal
        if search_problem.goal_test(current_state):
            solution.path = backchain(current_node)
            solution.cost = current_node.cost

            return solution

        # Now following the pseudocode from Lecture 6:
        for child_state in search_problem.get_successors(current_state):
            child_transition_cost = search_problem.get_cost(current_state, child_state) + current_node.cost

            # If child not in explored or child is in frontier with higher f
            if child_state not in visited_cost or child_transition_cost < visited_cost[child_state]:
                # Add child to explored
                visited_cost[child_state] = child_transition_cost

                # Pack child state into a node, with backpointer to current_node
                child_node = AstarNode(child_state, heuristic_fn(child_state), current_node, child_transition_cost)

                # Add the node to the frontier
                heappush(pqueue, child_node)

    return solution
