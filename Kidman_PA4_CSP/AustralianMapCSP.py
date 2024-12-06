# Author: Lauren Kidman
# Date: 18 November 2024
# COSC 76: Artificial Intelligence 24F

class AustralianMapCSP:
    def __init__(self):
        """
        Summary: Initializes the Australian Map CSP problem with variables, domains, and constraints

        Australian Map Problem:
        No Australian regions that are next to each other/neighbors may have the same color
        """
        self.problem_type = "map_coloring"  # This will be used for is_legal in the general CSP solver

        # To work in numbers, I defined the regions' letters as their corresponding numbers based on a phone dial
        self.variables = [92, 68, 72, 78, 679, 84, 82]  # WA, NT, SA, Q (QU), NSW, V (VI), T (TA)

        # Define the domain for each region as numbers corresponding to the colors red, green, blue
        # 1: red, 2: green, 3: blue
        self.domains = {}
        for var in self.variables:
            self.domains[var] = [1, 2, 3]

        # Hardcode in constraints based on the map of Australian regions:
        self.constraints = {
            92: [68, 72],  # WA cannot have the same color as NT or SA
            68: [92, 72, 78],  # NT cannot have the same color as WA, SA, or Q
            72: [92, 68, 78, 679, 84],  # SA cannot have the same color as WA, NT, Q, NSW, or V
            78: [68, 72, 679],  # Q cannot have the same color as NT, SA, or NSW
            679: [72, 78, 84],  # NSW cannot have the same color as SA, Q, or V
            84: [72, 679],  # V cannot have the same color as SA or NSW
            82: []  # T has no neighbors (so can have any color)
        }

    def is_constraint_satisfied(self, val1, val2):
        """
        Summary: Checks if the given values (colors) satisfy the map coloring constraint -- i.e. Neighboring regions
        should not have the same color
        """
        # Map coloring constraint: Neighboring regions should not have the same color
        return val1 != val2

    # Output method that takes solutions to the integer CSP, and print them out nicely using territory names and colors
    def format_nums_to_text(self, assignment):
        """
        Summary: Converts the numeric assignment of regions and colors to letter-based
        region names and color names for easier interpretation/readability
        """
        # Define the mapping from numbers to region names
        region_map = {
            92: "WA",
            68: "NT",
            72: "SA",
            78: "Q",
            679: "NSW",
            84: "V",
            82: "T"
        }

        # Define the mapping from numbers to color names
        color_map = {
            1: "Red",
            2: "Green",
            3: "Blue"
        }

        # Now loop through all the number results from assignment and match nums to text
        nums_to_text = {}

        for region, color in assignment.items():
            region_name = region_map[region]
            color_text = color_map[color]

            nums_to_text[region_name] = color_text

        return nums_to_text
