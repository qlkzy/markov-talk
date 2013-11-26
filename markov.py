#! /usr/bin/env python2
"""
Markov Chain Text Generator

Usage:
    markov [-s seed] [-n order] [--] [<file>...]

Options:
    -s <s> Seed for the random number generator
    -n <n> Number of previous words to consider when choosing the next word [default: 1]

"""

import random
import fileinput
import sys
from docopt import docopt
from time import time

class Example:

    def __init__(self, pat, succ):
        self.pat = list(pat)
        self.succ = succ

    def suffix_of(self, seq):
        if not seq:
            return True
        n = min(len(seq), len(self.pat))
        return cmp(seq[-n:], self.pat[-n:]) == 0

def succ(seq, examples):
    cands = [e.succ for e in examples if e.suffix_of(seq)]
    if not cands:
        sys.stderr.write("restart\n")
        cands = [e.succ for e in examples]
    return random.choice(cands)

def gen(seq, examples):
    seq = list(seq)
    seq.append(succ(seq, examples))
    return seq

def train(n, training_data):
    window = []
    examples = []
    for line in training_data:
        line = line.rstrip()
        examples.append(Example(window, line))
        window.append(line)
        if len(window) > n:
            window.pop(0)
    return examples
 


arguments = docopt(__doc__)

order = arguments["-n"]

try:
    seed = int(arguments["-s"])
except:
    seed = int(time())

random.seed(seed)

print seed

training_data = fileinput.input(arguments["<file>"])
examples = train(order, training_data)
print "trained"

out = []
for i in range(0, 100):
    print i
    out = gen(out, examples)

print ' '.join(out)
