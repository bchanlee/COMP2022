"""
USYD CODE CITATION ACKNOWLEDGEMENT
I declare that the following code has been copied from a provided code scaffold
of COMP2123 Assignment 4 with major changes to follow the specifications
of this assignment.
"""

from vertex import Vertex
from edge import Edge

class Graph:
    """
    Represents the automaton

    Attributes:
        * vertices (list): list of states
    """

    def __init__(self):
        """
        Initialises an empty graph
        """
        self.vertices = []

    def insert_vertex(self, name):
        """
        Insert the state storing the name

        :param name: the state name
        :return: The new vertex, also stored in the graph.
        """

        v = Vertex(name)
        self.vertices.append(v)
        return v

    def insert_edge(self, s, c, t):
        """
        Inserts the edge between state s and t with symbol c.

        :param s: previous state s
        :param c: alphabet symbol c
        :param t: following state t
        :return: The new edge between s and t with symbol c.
        """

        e = Edge(s, c, t)

        # check that edge doesn't already exist
        for i in s.edges:
            if i == e:
                return e

        s.add_edge(e)

        return e

    def DFS(self, start):
        """
        depth first search of the states, prints its path

        :param start: start state
        """
        a = []
        b = []

        self.epsilon_visit(start, a, b)
        print("{}:{}".format(start.name, ','.join(b)))

    def epsilon_visit(self, u, visited, current_path):
        """
        visits states with epsilon transitions

        :param u: current state
        :param visited: list of visited states
        :param current_path: the current path of the search
        """

        visited.append(u)
        current_path.append(u.name)

        # check states reachable by u
        for e in u.edges:
            # check if transition is epsilon
            if e.c == '':
                if e.t not in visited:
                    # recurse the reachable states
                    self.epsilon_visit(e.t, visited, current_path)
