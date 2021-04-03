from parser import Parser
from sys import stdin
from graph import Graph
from vertex import Vertex

def make_automata(nfa):
    """
    helper function - constructs data structure for automata

    :param nfa: dictionary rep of automata
    :return: graph data structure of automata
    """

    automata = Graph()
    # add states
    for s in nfa['states']:
        automata.insert_vertex(s)

    # add transitions - O(n^2)
    for d in nfa['delta']:
        s_name, c, t_name = d
        # find the previous state in the transition
        for s in automata.vertices:
            if s_name == s.name:
                # find the following state in the transition
                for t in automata.vertices:
                    if t_name == t.name:
                        # insert transition (edge) to dfa
                        automata.insert_edge(s, c, t)
                        break

    return automata

def print_task_2(nfa, automata, final):
    """
    helper function - prints output for task 2

    :param nfa: dictionary rep of automata
    :param automata: graph data structure of automata
    :param final: list of final states
    """

    print(",".join(nfa['states']))
    print(",".join(nfa['alphabet']))
    print(nfa['start'])
    print(",".join(final))

    for state in automata.vertices:
        for e in state.edges:
            print(e)

    print('end')

def remove_epsilon_edge(automata):
    """
    helper function - removes epsilon edges in automata

    :param nfa: dictionary rep of automata
    :return: automata with no epsilon transitions
    """

    # traverse vertices - O(n)
    for state in automata.vertices:
        epsilon_edges = []
        # traverse reachable states - O(n)
        for e in state.edges:
            # check if transition is epsilon
            if e.c == '':
                epsilon_edges.append(e)
        # remove the epsilon edges - O(n)
        for e in epsilon_edges:
            state.remove_edge(e)

    return automata

def update_final(dfa, efnfa):
    """
    calculates the set of final states of DFA

    :param dfa: dfa data structure (Graph)
    :param efnfa: efnfa data structure (dictionary)
    :return: list of final states
    """

    final = []
    for state in dfa.vertices:
        for final_state in efnfa['final']:
            if final_state in state.name and state.name not in final:
                final.append("-".join(state.name))
                break
    return final

def print_task_3(state_names, efnfa, final, dfa):
    """
    helper function - prints output for task 3

    :param state_names: names of the set of states
    :param efnfa: dictionary rep of automata
    :param final: list of final states
    :param dfa: graph data structure of automata
    """

    print(",".join(state_names))
    print(",".join(efnfa['alphabet']))
    print(efnfa['start'])
    print(",".join(final))
    for state in dfa.vertices:
        for e in state.edges:
            print("{},{},{}".format("-".join(e.s.name), e.c, "-".join(e.t.name)))
    print('end')

def add_error_state(dfa, efnfa):
    """
    inserts error states to the dfa

    :param dfa: dfa data structure (Graph)
    :param efnfa: efnfa data structure (dictionary)
    :return: list of state names and dfa data structure
    """

    error_state = Vertex(['error']) # create error state
    error_edges = [] # list of edges to error state
    error_exists = False # check whether error state exists in dfa
    state_names = [] # list of state names

    for state in dfa.vertices:
        # change state name to assignment specifications
        state_names.append("-".join(state.name))
        # get symbols
        symbols = [e.c for e in state.edges]
        # check if state has transitions to error state
        if len(symbols) < len(efnfa['alphabet']):
            error_exists = True
            for a in efnfa['alphabet']:
                if a not in symbols:
                    dfa.insert_edge(state, a, error_state)

    # check if error state exists in dfa
    if error_exists == True:
        # add error state
        dfa.vertices.append(error_state)
        state_names.append("-".join(error_state.name))
        # add self-loop to error state
        for a in efnfa['alphabet']:
            dfa.insert_edge(error_state, a, error_state)

    return state_names, dfa

def make_dfa(efnfa, initial, automata):
    """
    makes Graph structure of DFA from efnfa Graph

    :param efnfa: dictionary rep of automata
    :param initial: initial state (Vertex)
    :param automata: Graph rep of automata
    :return: dfa (Graph)
    """

    # graph setup with initial state
    dfa = Graph()
    t = Vertex([initial.name])
    dfa.vertices.append(t)

    # traverse through the states
    i = 0
    while i < len(dfa.vertices):
        states_set = dfa.vertices[i] # current state

        layer_list = [] # list of reachable states
        symbol_list = [] # list of symbols for corresponding transitions

        # traverse the alphabet
        for a in efnfa['alphabet']:
            layer = []
            # go through individual state name
            for state_name in states_set.name:
                # find individual state
                for state in automata.vertices:
                    if state.name == state_name:
                        current_state = state
                        break
                # find reachable states from individual state
                for e in current_state.edges:
                    if a == e.c:
                        if e.t not in layer:
                            layer.append(e.t)

            # check if there are reachable states
            if len(layer) > 0:
                layer_list.append(layer)
                symbol_list.append(a)

        # make graph by traversing the list of reachable states
        j = 0
        while j < len(layer_list):
            name = [v.name for v in layer_list[j]]
            name.sort() # sorted order of state names
            new_state = Vertex(name) # create vertex with set as the name
            # check if new state has been 'visited'
            if new_state not in dfa.vertices:
                dfa.vertices.append(new_state)
            # add transition
            dfa.insert_edge(states_set, symbol_list[j], new_state)
            j += 1

        i += 1

    return dfa

def get_initial(automata, efnfa):
    """
    retrieve initial state of automata

    :param automata: Graph rep of automata
    :param efnfa: dict rep of automata
    :return: initial state (Vertex)
    """

    # traverse the states
    for state in automata.vertices:
        # check if state is initial
        if state.name == efnfa['start']:
            initial = state
            break

    return initial

def task_1(parser):
    """For each state of the NFA, compute the Epsilon closure and output
    it as a line of the form s:a,b,c where s is the state, and {a,b,c} is E(s)"""
    nfa = parser.parse_fa()

    # graph setup
    automata = make_automata(nfa)

    # epsilon closure - O(n^2)
    for s in automata.vertices:
        automata.DFS(s)

    print('end')

def task_2(parser):
    """Construct and output an equivalent Epsilon free NFA.
    The state names should not change."""
    nfa = parser.parse_fa()
    closures = parser.parse_closures()

    # graph setup
    automata = make_automata(nfa)

    # remove epsilon transitions
    automata = remove_epsilon_edge(automata)

    # add in required transitions
    final = nfa['final']
    for k in closures.keys(): # O(n)
        list = closures[k]
        if len(list) > 1:
            # get the state
            for state in automata.vertices: # O(n)
                if state.name == k:
                    u = state
                    break

            list.remove(k) # remove original state from closures

            # traverse the list
            for vertex in list: # O(n)
                if vertex in final and u.name not in final:
                    final.append(u.name)
                # find the vertex
                for state in automata.vertices: # O(n)
                    if state.name == vertex:
                        v = state
                # update the transition
                for e in v.edges:
                    # add transition
                    automata.insert_edge(u, e.c, e.t) # sometimes doubles edges

    # printing
    print_task_2(nfa, automata, final)

def task_3(parser):
    """Construct and output an equivalent DFA.
    The input is guaranteed to be an Epsilon Free NFA."""
    efnfa = parser.parse_fa()

    # graph setup
    automata = make_automata(efnfa)

    # get initial state - O(n)
    initial = get_initial(automata, efnfa)

    # make DFA from EFNFA (without error states)
    dfa = make_dfa(efnfa, initial, automata)

    # add in error state
    state_names, dfa = add_error_state(dfa, efnfa)

    # update final states
    final = update_final(dfa, efnfa)

    # print
    print_task_3(state_names, efnfa, final, dfa)

def task_4(parser):
    """For each string, output 1 if the DFA accepts it, 0 otherwise.
    The input is guaranteed to be a DFA."""
    dfa = parser.parse_fa()
    test_strings = parser.parse_test_strings() # list of strings
    automata = make_automata(dfa) # graph setup

    # get initial state - O(n)
    initial = get_initial(automata, dfa)

    # traverse each string
    for string in test_strings:
        # compute empty string
        if string == '':
            if initial.name in dfa['final']:
                print(1)
            else:
                print(0)
        else:
            # traverse the edges (transitions) using each char of the string
            i = 0
            state = initial
            while i < len(string):
                for e in state.edges:
                    if e.c == string[i]:
                        state = e.t # go to next state
                        i += 1 # go to next char in the string
                        break
            # check that the arrived state is a final state
            if state.name in dfa['final']:
                print(1)
            else:
                print(0)

if __name__ == '__main__':

    parser = Parser()
    command = parser.parse_command()

    if command == 'epsilon-closure':
        task_1(parser)
    elif command == 'nfa-to-efnfa':
        task_2(parser)
    elif command == 'efnfa-to-dfa':
        task_3(parser)
    elif command == 'compute-dfa':
        task_4(parser)
    else:
        print(f'Command {repr(command)} not recognised.')
