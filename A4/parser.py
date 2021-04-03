# This code was provided by the COMP2022 tutors.

import re
from sys import stdin

class Parser:
    """Combined parser and reader, takes a stream as input, outputs cfg/commands"""

    def __init__(self, stream=stdin):
        """Defaults to reading from sys.stdin"""
        self.stream = stream

    def parse_command(self):
        """Grab the next line from the stream."""
        return next(self.stream).strip()

    def read_section(self):
        """Collect lines from the stream until 'end' is read."""
        lines = []
        line = next(self.stream).strip()
        while line != 'end':
            lines.append(line)
            line = next(self.stream).strip()
        return lines

    def parse_cfg(self):
        """Read from the stream, return a dictionary representing the CFG.

        key 'variables' gives the set of variable symbols (as a list)
        key 'terminals' gives the set of terminal symbols (as a list)
        key 'start' gives the label of the start variable
        key 'rules' gives a list of (V, production) tuples, where production is a list

        You will want use this data to construct more suitable data structures.
        """
        lines = self.read_section()
        it = iter(lines)
        cfg = dict()
        # variables and terminals are comma separated, with no whitespace
        cfg['variables'] = re.sub('\s', '', next(it)).split(',')
        cfg['terminals'] = re.sub('\s', '', next(it)).split(',')
        cfg['start'] = next(it)
        # the remaining lines are rules V -> production
        cfg['rules'] = list()
        for line in it:
            v, production = line.split('->')
            v = v.strip()
            # separate on whitespace (excluding leading or trailing whitespace)
            production = re.sub('\s', ' ', production.strip())
            production = production.split(' ')
            cfg['rules'].append((v, production))
        return cfg

    def parse_test_strings(self):
        """Read from the stream, return a list of strings (to be tested)"""
        return self.read_section()

    def parse_test_string(self):
        return self.read_section()[0]

