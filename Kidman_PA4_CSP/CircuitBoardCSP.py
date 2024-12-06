# Author: Lauren Kidman
# Date: 18 November 2024
# COSC 76: Artificial Intelligence 24F

class CircuitBoardCSP:
    def __init__(self, width, height, components):
        """
        Summary: Initializes the circuit board CSP problem with the board dimensions,
        components, variables, domains, and constraints

        Circuit Board Problem:
        Given a rectangular circuit board of size n x m, and k rectangular components of arbitrary sizes,
        lay the components out in such a way that they do not overlap
        """
        self.problem_type = "circuit_board"  # This will be used for is_legal in the general CSP solver

        self.board_width = width
        self.board_height = height
        self.components = components

        components_length = len(components)
        self.variables = list(range(components_length))

        # Each component in circuit is constrained by each other component
        # Create a dictionary to store list of other components each component cannot overlap with (excluding itself)
        self.constraints = {}
        for curr_component_index in range(components_length):
            current_constraints = []
            for other_component_index in range(components_length):
                if other_component_index != curr_component_index:
                    current_constraints.append(other_component_index)
            self.constraints[curr_component_index] = current_constraints

            # Default to no assignments
            self.assignment = {}
            for assign in self.variables:
                self.assignment[assign] = None

        # Domain for each component should be all possible positions it can fit into
        self.domains = {}
        for component_index in range(components_length):
            current_domain = []
            component_width, component_height = self.components[component_index]

            for possible_x in range(self.board_width + 1 - component_width):
                for possible_y in range(self.board_height + 1 - component_height):
                    current_domain.append((possible_x, possible_y))  # Coordinates taking the form (x,y) (tuples)
            self.domains[component_index] = current_domain

    def is_constraint_satisfied(self, var1, pos1, var2, pos2):
        """
        Summary: Checks if the given component locations satisfy the Circuit Board constraint -- i.e. ensuring placing
        component 1 at position 1 and component 2 at position 2 does not result in overlap
        """
        x1, y1 = pos1
        x2, y2 = pos2
        width1, height1 = self.components[var1]
        width2, height2 = self.components[var2]

        # Check for overlap between rectangles
        if x1 + width1 <= x2 or x2 + width2 <= x1 or y1 + height1 <= y2 or y2 + height2 <= y1:
            return True  # No overlap

        return False  # Overlap detected

    def format_nums_to_text(self, assignment):
        """
        Summary: Creates a circuit board of '.' with proper dimensions, converting component indices into ASCII letters
        to differentiate each component in the list
        """
        # First create an empty board filled with '.'
        board = []
        for r in range(self.board_height):
            row = []
            for c in range(self.board_width):
                row.append('.')
            board.append(row)

        # Place each component, in letter form, on the board:
        for component_index, (x, y) in assignment.items():
            component_width, component_height = self.components[component_index]

            # Iterate over each space the component occupies, based on its size
            for dx in range(component_width):
                for dy in range(component_height):
                    # To assign the component a unique letter placeholder, use num to ASCII conversion and add the index
                    # of the current component to make the letters unique for each component
                    board[y + dy][x + dx] = chr(65 + component_index)

        # Finally print out the board, row by row
        for row in board:
            print("".join(row))
