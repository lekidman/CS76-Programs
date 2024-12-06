# Author: Lauren Kidman
# Date: 18 October 2024
# COSC 76: Artificial Intelligence 24F

import math

from Maze import Maze
from time import sleep


class MazeworldProblem:
    """
    Summary: Represents a maze problem for multiple robots navigating towards their goal states,
    moving north/south/east/west/stay one at a time

    Attributes:
        maze: The maze environment (.maz file)
        start_state: The initial state of the robots
        goal_state: The target locations for the robots
        num_robots: The number of robots in the maze
       """
    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        # Given it is a multi-robot coordination problem, by default start with robot with the first turn:
        # Similarly, unpack the array of robot locations to start
        self.start_state = tuple([0] + self.maze.robotloc)
        # Assuming goal_locations takes the form: [x1,y1,x2,y2] etc.
        self.num_robots = len(goal_locations) // 2
        self.goal_state = goal_locations

    def __str__(self):
        string = "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        """
        Summary: "Animate" the path taken by the robots through the maze

        :param path: A list of states representing the path the robots took to their goal states
        """
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))

    # Manhattan heuristic only allows horizontal and vertical movement, like in a grid
    def manhattan_heuristic(self, state):
        """
        Summary: Calculate the Manhattan (grid-moving) distance heuristic for a given state

        :param state: The current state of the robots and the turn indicator
        :return: The total Manhattan distance to the goal state
        """
        total_distance_manhattan = 0
        # Loop starts at 1 to skip turn indicator in the tuple
        for step in range(1, len(state), 2):
            x1, y1 = state[step], state[step + 1]
            x2, y2 = self.goal_state[step - 1], self.goal_state[step]

            total_distance_manhattan += abs(x2 - x1) + abs(y2 - y1)

        return total_distance_manhattan

    # Euclidian heuristic is the straight-line distance between two points -- for fun
    def euclidian_heuristic(self, state):
        """
        Summary: Calculate the Euclidean distance ((x^2+y^2)^(1/2)) heuristic for a given state

        :param state: The current state of the robots and the turn indicator
        :return: The total Euclidean distance to the goal state
        """
        total_distance_euclidian = 0
        # Move through the loop by 2 to make x and y coordinate breakdown consistent
        for step in range(1, len(state), 2):
            x1, y1 = state[step], state[step + 1]
            x2, y2 = self.goal_state[step - 1], self.goal_state[step]

            total_distance_euclidian += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return total_distance_euclidian

    def get_successors(self, states_tuple):
        """
        Summary: Generates successor states from the current state by moving the active robot

        Representation of grid of neighbors: (possible moves are up, down, left, right, stay)"
              ---   (x,y+1)   ---
            (x-1,y)  <x,y>  (x+1,y)
              ---   (x,y-1)   ---

        :param states_tuple: The current state of the robots (in tuple form)
        :return: A list of tuples representing the successor states
        """
        successors = []

        active_robot = states_tuple[0]  # Tells us which robot's turn we are on
        next_robot = int((active_robot + 1) % self.num_robots)  # Add 1 to move to the next robot's turn

        # Get current coordinates
        x = states_tuple[active_robot * 2 + 1]
        y = states_tuple[active_robot * 2 + 2]

        actions = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1), (x, y)]
        for move in actions:
            x_new = move[0]
            y_new = move[1]

            # Now move, while checking for collisions with current robot positions + staying within bounds:
            if self.maze.is_floor(x_new, y_new):
                no_collision = True
                for index in range(1, len(states_tuple), 2):
                    # Now handling collision scenarios:
                    # If the current index matches the index of the active robot, skip to avoid self-collision
                    if index == active_robot * 2 + 1:
                        continue
                    # If the new coordinates are already occupied by a robot, indicate collision
                    if x_new == states_tuple[index] and y_new == states_tuple[index + 1]:
                        no_collision = False
                        break

                # If no collision detected:
                if no_collision:
                    # Since tuples are immutable, we create a list duplicate of the old states to modify
                    successor_states = list(states_tuple)

                    successor_states[active_robot * 2 + 1] = x_new
                    successor_states[active_robot * 2 + 2] = y_new
                    successor_states[0] = next_robot

                    successors.append(tuple(successor_states))

        return successors

    # Let's make the cost function the total fuel expended by the robots.
    # A robot expends one unit of fuel if it moves, and no fuel if it waits a turn.
    def get_cost(self, current_state, child_state):
        """
        Summary: Calculate the cost of moving from the current state to the child state,
        cost is based on the "fuel" expended by the robots (1 if move, 0 if not)

        :param current_state: The current state of the robots
        :param child_state: The proposed next state of the robots
        :return: The cost associated with moving to the child state
        """
        # To check if the robot has moved or stayed, all we need to do is see if any of the
        # states have changed between the parents and child tuple (ignoring turn indicator)
        if current_state[1:] != child_state[1:]:
            return 1
        return 0

    def goal_test(self, current_state):
        """
        Summary: Check if the current state is a goal state

        :param current_state: The current state of the robots
        :return: True if all robots are at their goal locations, False otherwise
        """
        return current_state[1:] == self.goal_state


# A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
