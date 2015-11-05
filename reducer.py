#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = []
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count.append(count)
    else:
        if current_word:
            # write result to STDOUT. The result records what movies a user has watched
            print '%s\t%s' % (current_word, ','.join(current_count))
        current_count = [count]
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s' % (current_word, ','.join(current_count))

