# Author: Lauren Kidman
# Date: 18 November 2024
# COSC 76: Artificial Intelligence 24F

import math
from collections import deque


class ConstraintSatisfactionProblem:
    def __init__(self, csp):
        """
        Summary: Initializes the CSP solver with the given problem and sets up a counter for states visited
        """
        self.csp = csp
        self.states_visited = 0
        self.backtracks = 0

    # Following the pseudocode in Lecture 10, backtracking is the heart of CSP
    def backtracking_search(self, use_mrv, use_lcv, use_degree, use_ac3):
        """
        Summary: Calls the recursive backtracking algorithm, passing in if heuristics + inferences are to be used
        """
        return self.call_backtrack({}, use_mrv, use_lcv, use_degree, use_ac3)

    def call_backtrack(self, assignment, use_mrv, use_lcv, use_degree, use_ac3):
        """
        Summary: The recursive backtracking function that tries to find a valid assignment for the CSP
        """
        # As base case for recursion, check if the assignment is complete:
        if self.is_complete(assignment):
            return assignment

        # Otherwise, select the next variable to assign based on use statements
        variable = self.select_next(assignment, use_mrv, use_degree)

        # Order values of the selected variable based on use statements
        values = self.order_values(assignment, variable, use_lcv)

        # Try each value in the domain of the selected variable
        for value in values:
            # Increment the states_visited counter each time we try a new assignment -- for testing
            self.states_visited += 1

            if self.is_legal(variable, value, assignment):
                assignment[variable] = value

                # Apply inference, if enabled
                inferences = self.apply_inference(assignment, variable, use_ac3)

                # If inference is not failure
                if inferences is not None:
                    # Continue with backtracking
                    result = self.call_backtrack(assignment, use_mrv, use_lcv, use_degree, use_ac3)
                    if result is not None:
                        return result

                # Otherwise, if inference fails or result is failure, remove value from assignment
                assignment[variable] = None
                self.backtracks += 1

        # If no value leads to a solution, return failure
        return None

    def is_complete(self, assignment):
        """
        Summary: Checks if the assignment is complete -- i.e. all variables are assigned
        """
        # Loop through each variable in the CSP:
        for var in self.csp.variables:
            # If any variable is not in the assignment, csp is not complete
            if var not in assignment or assignment[var] is None:
                return False

        return True

    def select_next(self, assignment, use_mrv, use_degree):
        """
        Summary: Selects the next variable to assign based on heuristics--MRV, degree, or both--otherwise return first
        unassigned variable
        """
        # First find and store unassigned variables
        unassigned_variables = []

        for unassigned in self.csp.variables:
            if unassigned not in assignment or assignment[unassigned] is None:
                unassigned_variables.append(unassigned)

        # If no variables are unassigned, return None
        if not unassigned_variables:
            return None

        # If use_mrv is set to True, now use MRV heuristic to find the unassigned variable with the min # remaining vals
        if use_mrv:
            # print("Applying MRV heuristic")
            min_remaining_values = float(math.inf)
            candidate = []

            for var in unassigned_variables:
                # Count the number of legal states in the domain of the current variable
                num_values = len(self.csp.domains[var])
                # If the number of legal values is less than the current minimum:
                if num_values < min_remaining_values:
                    min_remaining_values = num_values
                    candidate = [var]
                # If there is a tie, add the second variable as a candidate
                elif num_values == min_remaining_values:
                    candidate.append(var)

            # If degree heuristic is True and there is a tie, choose variable with most constraints on remaining vars
            if use_degree and len(candidate) > 1:
                # print("Applying Degree heuristic")
                max_constraints = -1
                selected_variable = None

                # Loop through each candidate and count its number of constraints with unassigned neighbors
                for can in candidate:
                    curr_constraints = 0
                    for neighbor in self.csp.constraints[can]:
                        if neighbor not in assignment:
                            curr_constraints += 1

                    # If current candidate has more constraints than the current max, make it the new final selection
                    if curr_constraints > max_constraints:
                        max_constraints = curr_constraints
                        selected_variable = can

                # Return the tie-breaker candidate with max constraints
                # print(f"Degree heuristic selected: {selected_variable}")
                return selected_variable

            # If no tiebreaker or use_degree is False, return first candidate in list
            # print(f"MRV heuristic selected: {candidate[0]}")
            return candidate[0]

        # If no heuristics are used (use_mrv and use_degree = False), return first unassigned_variable
        # print("No heuristics applied, selecting first unassigned variable")
        return unassigned_variables[0]

    def order_values(self, assignment, variable, use_lcv):
        """
        Summary: Orders the values for the selected variable based on the LCV heuristic if enabled,
        otherwise simply returns the default list order
        """

        if use_lcv:
            # print("Applying LCV")
            # Initialize a dictionary to count # of constraints imposed by each value on neighboring variables
            value_constraint_count = {}
            for value in self.csp.domains[variable]:
                value_constraint_count[value] = 0

            # Iterate through all neighbors of the current variable
            for neighbor in self.csp.constraints[variable]:
                # Only consider neighbors that are not yet assigned
                if neighbor not in assignment:
                    for value in self.csp.domains[neighbor]:
                        # If the value of the current variable is also a value for a neighbor, increment
                        if value in value_constraint_count:
                            value_constraint_count[value] += 1

            # Sort values based on the (least) number of constraints they impose
            # print("Returning sorted LCV values")
            return sorted(value_constraint_count, key=lambda v: value_constraint_count[v])

        # Otherwise simply return values in default order
        # print("Returning default order")
        return self.csp.domains[variable]

    def is_legal(self, variable, value, assignment):
        """
        Summary: Checks if assigning a value to a variable is consistent with all constraints
        defined by each specific problem context
        """
        for neighbor in self.csp.constraints[variable]:
            if neighbor in assignment:
                if self.csp.problem_type == "map_coloring":
                    # Map coloring problem: Check if the colors are different
                    if not self.csp.is_constraint_satisfied(value, assignment[neighbor]):
                        return False
                elif self.csp.problem_type == "circuit_board":
                    # Circuit board problem: Check for overlap
                    if not self.csp.is_constraint_satisfied(variable, value, neighbor, assignment[neighbor]):
                        return False

        return True

    # Following pseudocode from textbook/Lecture 10 slides:
    def apply_inference(self, assignment, variable, use_ac3):
        """
        Summary: Applies the AC-3 inference algorithm if enabled, otherwise does nothing
        """
        if use_ac3:
            if self.ac3():
                # print("AC-3 made changes to the domains:")
                return {}
            else:
                # print("AC-3 failed, returning None")
                return None

        return {}

    def ac3(self):
        """
        Summary: Implements the AC-3 algorithm to enforce "arc consistency" in the CSP
        """
        queue = deque()
        for curr_var in self.csp.variables:
            for neighbor_var in self.csp.constraints[curr_var]:
                queue.append((curr_var, neighbor_var))

        while queue:
            curr_var, neighbor_var = queue.popleft()
            if self.revise(curr_var, neighbor_var):
                if len(self.csp.domains[curr_var]) == 0:
                    return False
                for adjacent_var in self.csp.constraints[curr_var]:
                    if adjacent_var != neighbor_var:  # "for each Xk in Xi.NEIGHBORS - {Xj}"
                        queue.append((adjacent_var, curr_var))

        return True

    def revise(self, curr_var, neighbor_var):
        """
        Summary: Helper function to ac3 -- revises the domain of a variable to enforce consistency with a neighbor
        """
        revised = False

        for value in self.csp.domains[curr_var][:]:
            # Assuming the value is not consistent with any value in the neighbor's domain...
            is_consistent = False

            # Check if there's at least one value in the neighbor's domain that satisfies the constraint
            for neighbor_val in self.csp.domains[neighbor_var]:
                if value != neighbor_val:  # !!This is the map coloring constraint -- no two colors next to each other!!
                    is_consistent = True
                    break  # Once one match is found, the loop can finish

            # If there's no value that satisfies the constraint, remove the value
            if not is_consistent:
                self.csp.domains[curr_var].remove(value)
                revised = True

        return revised

    def get_states_visited(self):
        """
        Summary: Returns the number of states visited during the search, to use for testing
        """
        return self.states_visited

    def get_backtrack_count(self):
        """
        Summary: Returns the number of times the solver had to backtrack, to use for testing
        """
        return self.backtracks
