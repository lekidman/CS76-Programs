# Author: Lauren Kidman
# Date: 4 October 2024
# COSC 76: Artificial Intelligence 24F
class FoxProblem:
    """
    Summary: A class to represent the chickens and foxes problem, where the goal is to safely move all animals across
    the river while abiding by the game rules (never fewer chickens than foxes on either side).

    Attributes:
        start_state (tuple): A tuple representing the initial number of chickens, foxes,
            and the boat's location (1 for left, 0 for right).
        goal_state (tuple): A tuple representing the target state (0, 0, 0), i.e. when all animals are moved to the right.
        total_chickens (int): The total number of chickens in the initial state.
        total_foxes (int): The total number of foxes in the initial state.
    """
    def __init__(self, start_state=(3, 3, 1)):  # we will assume that 1 represents left side, 0 is right side
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_chickens = start_state[0]
        self.total_foxes = start_state[1]

    def get_successors(self, state):
        """
            Summary: Generates all possible successor states from the current state, depending on the
            boat's location (left or right).

            :param state: A tuple representing the current state (chickens on the left, foxes on the left, boat location).

            :return: A list of valid successor states from the current state.
        """
        successors = []
        boat = state[2]

        # Possible combinations given that the boat can only hold up to 2 animals at a time:
        actions = [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]

        # The easiest place to start implementing the rules is the boat, which only switches between 1 and 0
        for action in actions:
            if boat == 1:  # Boat is on the left side
                next_state = ((state[0] - action[0]), (state[1] - action[1]), 0)
            else:
                # If boat is coming from right, that means chickens and or foxes are
                # being added back because the boat needs at least one animal to move
                next_state = ((state[0] + action[0]), (state[1] + action[1]), 1)

            # Now need to check if the new state is legal
            if self.is_safe(next_state):
                successors.append(next_state)

        return successors

    # This function is used to check each state against the rules of the game
    def is_safe(self, state):
        """
            Summary: A helper function to get_successors() that determines if a given state is "safe"
            according to the rules of the problem/filters out illegal states.

            A state is considered safe if:
                - The number of chickens is not less than the number of foxes on either side of the river (unless there
                are no chickens).
                - The number of chickens and foxes on both sides of the river must be within valid bounds (no negative
                numbers and no more than the starting total).

            :param state: A tuple representing the state to be assessed (chickens on the left, foxes on the left, boat location).

            :return: True if the state is safe (legal move), False otherwise.
        """
        left_chickens = state[0]
        right_chickens = self.start_state[0] - left_chickens
        left_foxes = state[1]
        right_foxes = self.start_state[1] - left_foxes

        # Now we do 2 checks (splitting it up for readability):

        # Check 1: cannot have more foxes than chickens on either side
        if (left_chickens < left_foxes and left_chickens != 0) or \
                (right_chickens < right_foxes and right_chickens != 0):
            return False

        # Check 2: cannot have more chickens or foxes than the starting state or any negative numbers
        if (left_chickens > self.total_chickens or left_foxes > self.total_foxes) or \
                (right_chickens > self.total_chickens or right_foxes > self.total_foxes):
            return False

        return True

    def goal_test(self, state):
        """
            Summary: A function to test if the current state is the goal state.

            :param state: A tuple representing the current state (chickens on the left, foxes on the left, boat location).

            :return: True if the current state matches the goal state, False otherwise.
        """
        if state == self.goal_state:
            return True

        return False

    def __str__(self):
        string = "Chickens and foxes problem: " + str(self.start_state)
        return string


# A bit of test code
if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
