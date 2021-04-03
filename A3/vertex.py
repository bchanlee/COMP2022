"""
USYD CODE CITATION ACKNOWLEDGEMENT
I declare that the following code has been copied from a provided code scaffold
of COMP2123 Assignment 4 with major changes to follow the specifications
of this assignment.
"""

class Vertex:
    """
    Represents a state in the automaton

    Attributes:
        * name (string): The state name
        * edges (list): The list of edges where this vertex is connected
    """

    def __init__(self, name):
        """
        Initialises the state on the automaton.

        :param name: cannot contain comma, colon, or whitespace characters
        """

        self.name = name
        self.edges = []

    def __eq__(self, state):
        """
        Overrides the equality

        :param state: The other state comparing to
        :return: Bool if equal
        """

        if isinstance(state, Vertex):
            return state.name == self.name

        return False

    def add_edge(self, e):
        """
        Adds the edge e to the set of edges.

        :param e: The new edge to add.
        """

        self.edges.append(e)

    def remove_edge(self, e):
        """
        Removes the edge from the set of edges.
        
        :param e: The edge to remove.
        """
        self.edges.remove(e)
