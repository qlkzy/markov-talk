#! /usr/bin/env python2
"""
Markov Chain Text Generator

Usage:
    markov [-s seed] [-n order] [-l length] [-r random] [--] [<file>...]

Options:
    -s <s> Seed for the random number generator
    -n <n> Number of previous words to consider when choosing the next word [default: 1]
    -l <l> Length of the desired output, in words
    -r <r> Probability (between 0 and 1) that a random token with no connection will be chosen

"""

import random
import fileinput
import sys
from docopt import docopt
from time import time
from itertools import islice
from time import sleep

class Example:

    def __init__(self, pat, succ):
        self.pat = list(pat)
        self.succ = succ

    def suffix_of(self, seq):
        if not seq:
            return True
        n = min(len(seq), len(self.pat))
        return cmp(seq[-n:], self.pat[-n:]) == 0

class Chain:

    def __init__(self, n, seed, randomness):
        self.n = n
        self.seed = seed
        self.randomness = randomness

    def train(self, training_data):
        self.examples = []
        window = []
        for tok in training_data:
            tok = tok
            self.examples.append(Example(window, tok))
            window.append(tok)
            if len(window) > self.n:
                window.pop(0)
    
    def __iter__(self):
        self.seq = []
        return self

    def next(self):
        cands = [e.succ for e in self.examples if e.suffix_of(self.seq)]
        if (not cands) or (random.random() < self.randomness):
            cands = [e.succ for e in self.examples]
        succ = random.choice(cands)
        self.seq.append(succ)
        return succ

arguments = docopt(__doc__)

try:
    order = int(arguments["-n"])
except:
    order = 1

try:
    seed = int(arguments["-s"])
except:
    seed = int(time())

try:
    length = int(arguments["-l"])
except:
    length = 100

try:
    randomness = float(arguments["-r"])
except:
    randomness = 0

random.seed(seed)

sys.stderr.write(str(seed) + "\n")

chain = Chain(order, seed, randomness)
chain.train(fileinput.input(arguments["<file>"]))

x = chain.__iter__()

for i in range(0, length):
    print chain.next(),
    
#print ' '.join(islice(chain, length))

