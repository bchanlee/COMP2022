"""
USYD CODE CITATION ACKNOWLEDGEMENT
I declare that the following code has been copied from a provided code scaffold
of COMP2123 Assignment 4 with major changes to follow the specifications
of this assignment.
"""

class Edge:
    """
    Represents the transitions between two states

    Attributes:
        * s (Vertex): The previous state
        * t (Vertex): The following state
        * c (string): the alphabet symbol
    """

    def __init__(self, s, c, t):
        """
        Initialises the directed edge with two vertices and symbol

        :param s: previous state s
        :param c: symbol for transition
        :param t: next state t
        """

        self.s = s
        self.t = t
        self.c = c

    def __eq__(self, edge):
        """
        Overrides the equality
        
        :param edge: The other edge comparing to
        :return: Bool if equal
        """

        if isinstance(edge, Edge):
            return (edge.s == self.s) and (edge.t == self.t) \
            and (edge.c == self.c)

        return False

    def __repr__(self):
        """
        Defines the string representation of the edge.
        """

        return "{},{},{}".format(self.s.name, self.c, self.t.name)
