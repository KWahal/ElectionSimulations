import numpy as np
import math
from random import seed
from random import random
import statistics
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from collections import Counter


def create_distribution():
    distributions = []
    for i in range(100000):
        distributions.append(random())

    # Find what the total sums to
    sum = 0
    for column in distributions:
        sum += column

    # Calculate middle index
    midpoint = sum/2
    new_sum = 0
    for i in range(len(distributions)):
        if new_sum < midpoint:
            new_sum += distributions[i]
        else:
            mid_index = i
            break

    # i represents the median
    left_candidate = random()*i
    right_candidate_one = random()*i+i
    right_candidate_two = random()*i+i
    if right_candidate_one < right_candidate_two:
        mid_candidate = right_candidate_one
        right_candidate = right_candidate_two
    else:
        mid_candidate = right_candidate_two
        right_candidate = right_candidate_two



    # GENERATE NORMAL ELECTION WINNER
    divider = (mid_candidate+right_candidate)/2

    print(sum)
    print(mid_index)
    print(left_candidate, " ", right_candidate_one, " ", right_candidate_two)



def main():
    create_distribution()

if __name__ == '__main__':
    main()