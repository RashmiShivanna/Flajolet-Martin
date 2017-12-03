import os
import random
import mmh3
import re
import numpy as np


def median(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    half = int(half)
    return sum(sorted(lst)[half:half + even]) / float(even)


class HashFunction:
    def __init__(self, seed):
        self.func = lambda x: (mmh3.hash(x, seed=seed) % 2 ** 20) + 1
        self.max_tail_count = 0


class HashGroup:
    def __init__(self, num_hashes_in_group=10):
        self.hash_functions = []
        for i in range(num_hashes_in_group):
            self.hash_functions.append(HashFunction(random.randint(1, 10000)))


class FlajoletMartinCounter:
    def __init__(self, num_hash_groups=10, num_hashes_in_group=10):
        self.hash_groups = []
        for i in range(num_hash_groups):
            self.hash_groups.append(HashGroup(num_hashes_in_group))

    def tail_length(self, num):
        """Counts the number of trailing 0 bits in num."""
        if num == 0:
            return 32  # Assumes 32 bit integer inputs!
        p = 0
        while (num >> p) & 1 == 0:
            p += 1
        return p

    def process(self, element):
        for g in self.hash_groups:
            for f in g.hash_functions:
                h = f.func(element)
                tail_count = self.tail_length(h)
                if tail_count > f.max_tail_count:
                    f.max_tail_count = tail_count

    def give_estimate(self):
        estimate_pr_group = []
        for g in self.hash_groups:
            estimate_in_group = []
            for f in g.hash_functions:
                estimate_in_group.append(2 ** f.max_tail_count)
            estimate_pr_group.append(np.mean(estimate_pr_group))
        return 1.0 * np.median(estimate_in_group)


#files = ['quotes_2008-08.txt','quotes_2008-09.txt','quotes_2008-10.txt','quotes_2008-11.txt','quotes_2008-12.txt','quotes_2009-01.txt','quotes_2009-02.txt','quotes_2009-03.txt','quotes_2009-04.txt']

text = "this is so hard and hard and this is now and last"
count = 0
# using Python set to estimate the number of distinct words in a Shakespeare text
Quotes = set()

# Using FM to estimate the number of distinct words in a Shakespeare text
FM = FlajoletMartinCounter(num_hash_groups=10, num_hashes_in_group=10)
for line in text.split(' '):
            line = re.sub(r'[^\w\s]', '', line[1:].lower())
            FM.process(line)
            Quotes.add(line)



print ("Number of quotes: "+str(count))
print ("Number of distinct quotes using FM: ",FM.give_estimate())
print ("Number of distinct quotes using python's set: ",(len(Quotes)))

