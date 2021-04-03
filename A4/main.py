from parser import Parser
from sys import stdin
from collections import deque

"""
Represents the CFG's rules as a dictionary, where keys are variables
and values are 2-D lists storing all possible rules for the variable
"""
def represent_rules(cfg):
    dictionary = {}
    i = 0
    # traverse the rules
    while i < len(cfg['rules']):
        # retrieve current variable and next variable from each rule
        current_var, next_var = cfg['rules'][i]
        # update dictionary
        if current_var not in dictionary.keys():
            dictionary[current_var] = [next_var]
        else:
            dictionary[current_var].append(next_var)
        i += 1

    return dictionary

"""
Makes a table according to the CYK algorithm
"""
def CYK_table(test_string, dictionary):
    # intitialise n x n table
    table = []
    n = len(test_string)
    for i in range(0, n):
        row = [{}] * n
        table.append(row)

    # examine each substring of length 1 from input
    table = CYK_char(test_string, dictionary, table, n)

    # examine the remaining substrings from input
    table = CYK_substring(dictionary, table, n)

    return table, n

"""
Modified CYK algorithm when input string is empty
"""
def CYK_empty_input(dictionary, start_var):
    rules = dictionary[start_var]
    rule_exists = 0
    # traverse rules for start variable
    for rule in rules:
        # check if start_var -> '' rule exists
        if rule[0] == 'epsilon':
            rule_exists = 1
            break

    print(rule_exists)

"""
Modified CYK algorithm for substring of length 1
"""
def CYK_char(input, dictionary, table, n):
    for i in range(0, n):
        char = input[i]
        # traverse each variable
        for var in dictionary.keys():
            rules = dictionary[var]
            # traverse each rule in the form A -> b
            for rule in rules:
                if len(rule) == 1:
                    # check if var -> substring is a rule
                    if rule[0] == char:
                        # place var, rule, index in table(i, i)
                        entry = (var, tuple(rule), -1, i, i)
                        if len(table[i][i]) == 0:
                            table[i][i] = {entry}
                        else:
                            table[i][i].add(entry)

    return table

"""
Modified CYK algorithm for the remaining substrings
"""
def CYK_substring(dictionary, table, n):
    # traverse each length of substring from 2 to n
    for l in range(2, n+1):
        # traverse the start position of substring from 0 to n-l
        for i in range(0, n-l+1):
            # retrieve end position of substring
            j = i + l - 1
            # traverse each possible split position
            for k in range(i, j): # j
                # traverse each rule in the form A -> BC
                for var in dictionary.keys():
                    rules = dictionary[var]
                    for rule in rules:
                        if len(rule) == 2:
                            # check if B and C are in previous entries
                            check_list = 0
                            for e in table[i][k]:
                                if rule[0] == e[0]:
                                    check_list += 1
                                    break

                            for e in table[k+1][j]:
                                if rule[1] == e[0]:
                                    check_list += 1
                                    break

                            # add A, BC, k, i, j to table[i][j]
                            if check_list == 2:
                                entry = (var, tuple(rule), k, i, j)
                                if len(table[i][j]) == 0:
                                    table[i][j] = {entry}
                                else:
                                    table[i][j].add(entry)

    return table

"""
Prints the rightmost derivations from a list of rules
"""
def print_derivations(var_list, rules_list):
    # create sequence of lines to represent rightmost derivation
    output_list = []
    output_list.append([var_list[0]])
    output_list.append(list(rules_list[0]))

    if len(rules_list) >= 2:
        for i in range(1, len(rules_list)):
            # retrieve most recent rightmost derivation
            cur = output_list[i]

            # retrieve the last occuring non-terminal
            for j in range(-1, -len(cur)-1, -1):
                if cur[j] in var_list:
                    break

            # separate the non-terminal from the rest of the derivation
            after = None
            prev = cur[:j]
            prev.extend(rules_list[i])
            if j < -1:
                after = cur[j+1:]
                prev.extend(after)

            # add new derivation to the sequence
            output_list.append(prev)

    # print each rightmost derivation
    for output in output_list:
        print("".join(output))

"""
Repeatedly uses a stack for rightmost derivations (type = der)
or to check ambiguity (type = amb)
"""
def use_stack(type, stack, table, is_ambiguous, var_list, rules_list):
    while len(stack) > 0:
        # pop top element
        top_element = stack.pop()
        # apply the rule
        var_list.append(top_element[0])
        rules_list.append(top_element[1])
        # retrieve k, i, j
        k = top_element[2]
        i = top_element[3]
        j = top_element[4]

        # if (A, i, j) is top element, apply rule A -> BC
        if i != j:
            counter = 0
            # ambiguous string if 1+ specified rules in entry
            seen_a = False
            for e in table[i][k]:
                if e[0] == top_element[1][0]:
                    if type == "amb":
                        if seen_a == True:
                            is_ambiguous = 1
                            break
                        seen_a = True

                    # push element (B, i, k)
                    stack.append(e)
                    if type == "der":
                        break

            seen_b = False
            for e in table[k+1][j]:
                if e[0] == top_element[1][1]:
                    if type == "amb":
                        if seen_b == True:
                            is_ambiguous = 1
                            break
                        seen_b = True

                    # push element (C, k+1, j)
                    stack.append(e)
                    if type == "der":
                        break

    if type == "amb":
        return is_ambiguous

    if type == "der":
        return var_list, rules_list

def membership(parser):
    """For each string, decide if it is in the language."""
    cfg = parser.parse_cfg()
    test_strings = parser.parse_test_strings()
    # represent the rules in a more efficient way
    dictionary = represent_rules(cfg)
    # retrieve start variable
    start_var = cfg['start']

    # traverse each input
    for test_string in test_strings:
        # apply algorithm to empty input
        if test_string == '':
            CYK_empty_input(dictionary, start_var)

        else:
            # make CYK table
            table, n = CYK_table(test_string, dictionary)

            # accept if start variable is in "last" entry of the table
            accept = 0
            for e in table[0][n-1]:
                if e[0] == start_var:
                    accept = 1
                    break

            print(accept)

    print('end')

def rightmost_derivation(parser):
    """
    Give a rightmost derivation of the string. String is always non-empty.
    """
    cfg = parser.parse_cfg()
    test_string = parser.parse_test_string()
    # represent the rules in a more efficient way
    dictionary = represent_rules(cfg)
    # retrieve start variable
    start_var = cfg['start']
    # make CYK table
    table, n = CYK_table(test_string, dictionary)

    # retrieve any start variable in the last entry of table (if present)
    start_list = []
    for e in table[0][n-1]:
        if e[0] == start_var:
            start_list.append(e)

    # initialise the stack, list of variables and rules
    stack = deque()
    var_list = []
    rules_list = []

    # check for membership (if start variable is in last table entry)
    if len(start_list) > 0:
        start = start_list[0]
        # push element (S, 1, n) onto stack
        stack.append(start)
        # repeat while stack is not empty
        var_list, rules_list = use_stack("der", stack, table, -1,
                                         var_list, rules_list)

        # print the derivations
        print_derivations(var_list, rules_list)

    print('end')

def ambiguous(parser):
    """For each string, decide if it is ambiguous in this grammar."""
    cfg = parser.parse_cfg()
    test_strings = parser.parse_test_strings()
    # represent the rules in a more efficient way
    dictionary = represent_rules(cfg)
    # retrieve start variable
    start_var = cfg['start']

    for test_string in test_strings:
        # make CYK table
        table, n = CYK_table(test_string, dictionary)

        # retrieve start variables from the last table entry (if present)
        start_list = []
        for e in table[0][n-1]:
            if e[0] == start_var:
                start_list.append(e)

        # initialise stack, list of variables and rules, is_ambiguous boolean
        stack = deque()
        var_list = []
        rules_list = []
        is_ambiguous = 0

        # check if there are more than one start variables in the last entry
        if len(start_list) > 1:
            is_ambiguous = 1

        elif len(start_list) == 1:
            for start in start_list:
                # push element (S, 1, n) onto stack
                stack.append(start)
                # repeat while stack is not empty
                is_ambiguous = use_stack("amb", stack, table, is_ambiguous,
                                         var_list, rules_list)

        print(is_ambiguous)

    print('end')

if __name__ == '__main__':

    parser = Parser()
    command = parser.parse_command()

    if command == 'membership':
        membership(parser)
    elif command == 'rightmost-derivation':
        rightmost_derivation(parser)
    elif command == 'ambiguous':
        ambiguous(parser)
    else:
        print(f'Command {repr(command)} not recognised.')
