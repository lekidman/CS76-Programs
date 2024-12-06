# Author: Lauren Kidman
# Date: 18 October 2024
# COSC 76: Artificial Intelligence 24F

from Maze import Maze
from time import sleep


class SensorlessProblem:
    """
    Summary: Initializes the SensorlessProblem with the given maze and goal state; establishes all potential
    starting positions of the robot within the maze by identifying floor vs wall

    :param maze: An instance of the Maze class, representing the maze structure.
    :param goal_state: A tuple representing the desired goal location for the robot.
   """

    ## You write the good stuff here:
    def __init__(self, maze, goal_state):
        self.maze = maze
        self.goal_state = goal_state

        # When we initialize the problem, we need to establish all potential starting positions of the robot:
        start_states = []
        for row in range(0, maze.width):
            for col in range(0, maze.height):
                if maze.is_floor(row, col):
                    start_states.append(row)
                    start_states.append(col)

        # Now convert to a tuple so it cannot be modified:
        self.start_state = tuple(start_states)

    def __str__(self):
        string = "Blind robot problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        """
        Summary: "Animate" the path taken by the robots through the maze

        :param path: A list of states representing the path the robots took to their goal states
        """
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))

    # For this maze problem, especially as mazes get large, we want the minimum path length
    def h1_min_manhattan(self, state):
        """
        Summary: Calculates the minimum Manhattan (grid-moving) distance from the robot's position to its corresponding goal

        :param state: A tuple containing the current position of the robot
        :return: The minimum Manhattan distance to the goal location for the robot
        """

        # Define initial manhattan distance
        x1, y1 = state[0], state[1]
        x2, y2 = self.goal_state[0], self.goal_state[1]
        min_distance_manhattan = abs(x2 - x1) + abs(y2 - y1)

        # Checking for minimum heuristic through remaining states
        for i in range(2, len(state), 2):
            x1_new, y1_new = state[i], state[i + 1]
            curr_distance_manhattan = abs(x2 - x1_new) + abs(y2 - y1_new)

            min_distance_manhattan = min(min_distance_manhattan, curr_distance_manhattan)

        return min_distance_manhattan

    def get_successors(self, state_tuple):
        """
        Summary: Generates successor states from the current state by moving the blind robot

        Representation of grid of neighbors: (possible moves are up, down, left, right)"
              ---   (x,y+1)   ---
            (x-1,y)  <x,y>  (x+1,y)
              ---   (x,y-1)   ---

        :param state_tuple: The current state of the robot (in tuple form)
        :return: A list of tuples representing the successor states
        """
        successors = []

        actions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for move in actions:
            # From PA instructions, use a set to eliminate duplicates
            possible_moves = set()

            for index in range(0, len(state_tuple), 2):
                x_move = move[0]
                y_move = move[1]

                x_new = state_tuple[index] + x_move
                y_new = state_tuple[index + 1] + y_move

                # If the next move exists on the floor, add it as a possibility
                if self.maze.is_floor(x_new, y_new):
                    possible_moves.add((x_new, y_new))
                # If not, meaning the robot has hit a wall, add the current state again
                else:
                    possible_moves.add((state_tuple[index], state_tuple[index + 1]))

            # After processing all possible positions, convert into a single tuple
            set_to_tuple_successor = tuple(coord for pos in possible_moves for coord in pos)

            successors.append(set_to_tuple_successor)

        return successors

    def get_cost(self, current_state, child_state):
        """
        Summary: Calculate the cost of moving from the current state to the child state;
        Unlike in Mazeworld, the robot will always move, so always a cost of 1

        :param current_state: The current state of the robots
        :param child_state: The proposed next state of the robots
        :return: The cost associated with moving to the child state
        """
        return 1

    def goal_test(self, state):
        return state == self.goal_state


# A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
