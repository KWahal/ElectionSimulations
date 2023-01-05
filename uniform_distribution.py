"""
This file assumes that voters are uniformly distributed across an interval. There is thus no selection of voters.
The file allows you to choose the number of candidates and randomly generates candidates. It calculates the winners of
a standard election (primary, first-past-the-post), and a ranked-choice voting election, as well as the extremism
levels of the winning candidates, using a uniform distribution.

It provides the option to provide a variety of visualizations, such as the proportion of voters that hold a particular
ranking system for candidates and scatter plots comparing the extremism levels for the two types of elections.
If you choose, it is relatively easy to modify this code such that you manually decide the candidates.
"""

import numpy as np
import math
from random import seed
from random import random
import statistics
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from collections import Counter

""" This function generates a given number of candidates randomly. """
def gen_candidates_uniform(num_candidates):
    candidates_original = []
    for i in range(num_candidates):
        candidates_original.append(random() * 20)
    candidates_sorted = sorted(candidates_original)
    print("The candidates are " + str(candidates_sorted))
    print("")
    return candidates_sorted

""" Given a list of candidates, this function recursively generates the RCV winner and polarization level. """
def find_RCV_winner_uniform(candidates):
    candidates = sorted(candidates)
    votes = {}
    votes[candidates[0]] = candidates[0]/20
    votes[candidates[len(candidates) - 1]] = (20 - candidates[len(candidates) - 1])/20
    for i in range(len(candidates) - 1):
        if candidates[i] not in votes:
            votes[candidates[i]] = 0
        if candidates[i+1] not in votes:
            votes[candidates[i+1]] = 0
        midpoint = (candidates[i] + candidates[i+1])/2
        votes[candidates[i]] += ((midpoint - candidates[i])/20)
        votes[candidates[i+1]] += ((candidates[i+1] - midpoint)/20)
    winner = max(votes, key=votes.get)
    if votes[winner] >= 0.5:
        print("The final RCV vote breakdown is " + str(votes))
        polarization = abs(10 - winner)
        return winner, polarization
    print("The initial RCV vote breakdown is " + str(votes))
    least_votes = min(votes, key=votes.get)
    candidates.remove(least_votes)
    return find_RCV_winner_uniform(candidates)

""" This function generates the RCV vote rankings. """
def generate_voter_choices_uniform(candidates):
    # generate dictionary, with key as all midpoints, value as tuple of the respective candidates it is between
    midpoints = {}
    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            midpoint = (candidates[i] + candidates[j])/2
            if midpoint not in midpoints:
                midpoints[midpoint] = []
            t1 = (candidates[i], candidates[j])
            midpoints[midpoint].append(t1)
    midpoints = {key:value for key, value in sorted(midpoints.items(), key=lambda item: int(item[0]))}

    candidate_copy = candidates
    ultimate_votes = {}
    last_midpoint = 0
    for mid in midpoints: # iterate through keys, which are the midpoints
        size = abs((mid - last_midpoint)*5) # turn area into percentages
        # create key as a string with the candidate numbers rounded
        new_vote = ""
        for i in range(len(candidate_copy)):
            new_vote += str(round(candidate_copy[i], 2)) + " "
        ultimate_votes[new_vote] = size
        list = midpoints[mid]
        # swap as much as needed
        for j in range(len(list)):
            t1 = list[j]
            candidate_one = t1[0]
            candidate_two = t1[1]
            idx_one = candidate_copy.index(candidate_one)
            idx_two = candidate_copy.index(candidate_two)
            candidate_copy[idx_one] = candidate_two
            candidate_copy[idx_two] = candidate_one
        last_midpoint = mid # recalculate pointer

    size = abs((20 - last_midpoint)*5)
    new_vote = ""
    for i in range(len(candidate_copy)):
        new_vote += str(round(candidate_copy[i], 2)) + " "
    ultimate_votes[new_vote] = size

    return ultimate_votes


""" This function generates the CES system (primary, general election) winner and polarization level, given
a list of candidates """
def find_normal_winner_uniform(candidates):
    candidates = sorted(candidates)
    left_candidates = []
    right_candidates = []
    for i in range(len(candidates)):
        if candidates[i] < 10:
            left_candidates.append(candidates[i])
        if candidates[i] >= 10:
            right_candidates.append(candidates[i])

    if len(left_candidates) == 0:
        print("There is no left primary")
        right_winner = find_right_winner_uniform(right_candidates)
        ultimate_winner = right_winner
        polarization = abs(10 - ultimate_winner)
        return ultimate_winner, polarization
    elif len(right_candidates) == 0:
        print("There is no right primary")
        left_winner = find_left_winner_uniform(left_candidates)
        ultimate_winner = left_winner
        polarization = abs(10 - ultimate_winner)
        return ultimate_winner, polarization
    elif len(left_candidates) == 1:
        left_winner = left_candidates[0]
        print("The left winner is " + str(left_winner))
        right_winner = find_right_winner_uniform(right_candidates)
    elif len(right_candidates) == 1:
        right_winner = right_candidates[0]
        print("The right winner is " + str(right_winner))
        left_winner = find_left_winner_uniform(left_candidates)
    else:
        left_winner = find_left_winner_uniform(left_candidates)
        right_winner = find_right_winner_uniform(right_candidates)

    votes = {}
    votes[left_winner] = left_winner
    midpoint = (left_winner + right_winner)/2
    votes[left_winner] += midpoint - left_winner
    votes[right_winner] = 20 - right_winner
    votes[right_winner] += right_winner - midpoint

    ultimate_winner = max(votes,key=votes.get)
    polarization = abs(10 - ultimate_winner)
    print("The ultimate winner in a normal election is " + str(ultimate_winner))
    return ultimate_winner, polarization

"""
This function generates the left primary winner.
"""
def find_left_winner_uniform(left_candidates):
    votes = {}
    votes[left_candidates[0]] = left_candidates[0] / 10
    votes[left_candidates[len(left_candidates) - 1]] = (10 - left_candidates[len(left_candidates) - 1]) / 10
    for i in range(len(left_candidates) - 1):
        if left_candidates[i] not in votes:
            votes[left_candidates[i]] = 0
        if left_candidates[i + 1] not in votes:
            votes[left_candidates[i + 1]] = 0
        midpoint = (left_candidates[i] + left_candidates[i + 1]) / 2
        votes[left_candidates[i]] += ((midpoint - left_candidates[i]) / 10)
        votes[left_candidates[i + 1]] += ((left_candidates[i + 1] - midpoint) / 10)

    winner = max(votes, key=votes.get)
    print("The left winner is " + str(winner))
    return winner

"""
This function generates the right primary winner.
"""
def find_right_winner_uniform(right_candidates):
    votes = {}
    votes[right_candidates[0]] = (right_candidates[0] - 10) / 10
    votes[right_candidates[len(right_candidates) - 1]] = (20 - right_candidates[len(right_candidates) - 1]) / 10
    for i in range(len(right_candidates) - 1):
        if right_candidates[i] not in votes:
            votes[right_candidates[i]] = 0
        if right_candidates[i + 1] not in votes:
            votes[right_candidates[i + 1]] = 0
        midpoint = (right_candidates[i] + right_candidates[i + 1]) / 2
        votes[right_candidates[i]] += ((midpoint - right_candidates[i]) / 10)
        votes[right_candidates[i + 1]] += ((right_candidates[i + 1] - midpoint) / 10)

    winner = max(votes, key=votes.get)
    print("The right winner is " + str(winner))
    return winner

"""
This function puts together the earlier functions to generate the RCV and normal election winners
and polarization levels, and prints the results.
"""
def all_uniform_distribution(num_candidates):
    candidates = gen_candidates_uniform(num_candidates)
    normal_system = find_normal_winner_uniform(candidates)
    RCV_system = find_RCV_winner_uniform(candidates)
    print("The winner in the normal system is " + str(normal_system[0]))
    print("The polarization in the normal system is " + str(normal_system[1]))
    print("The winner in the RCV system is " + str(RCV_system[0]))
    print("The polarization in the RCV system is " + str(RCV_system[1]))

"""
This function graphs the polarization levels for RCV and normal, given a number of candidates
and number of times the function is run. 
"""
def graph_uniform_results(num_candidates, num_run):
    x = []
    y = []

    for i in range(num_run):
        candidates = gen_candidates_uniform(num_candidates)
        normal_system = find_normal_winner_uniform(candidates)
        RCV_system = find_RCV_winner_uniform(candidates)

        x.append(normal_system[1])
        y.append(RCV_system[1])

    plt.scatter(x, y, color="purple")

    plt.xlabel('Normal Election Polarization')
    plt.ylabel('Ranked Choice Voting Polarization')
    plt.title('RCV vs. First-Past-The-Post Primary Polarization')
    plt.show()

"""
This function generates the histogram for how voters rank their choices.
"""
def make_hist_uniform_rcv(num_candidates):
    candidates = gen_candidates_uniform(num_candidates)
    dict_graphing = generate_voter_choices_uniform(candidates)

    normal_system = find_normal_winner_uniform(candidates)
    RCV_system = find_RCV_winner_uniform(candidates)

    normal_polarization = normal_system[1]
    rcv_polarization = RCV_system[1]

    if rcv_polarization < normal_polarization:
        plt.bar(list(dict_graphing.keys()), dict_graphing.values(), color='g')
        plt.title('RCV < First-Past-The-Post Primary Polarization')
        plt.show()
    elif rcv_polarization == normal_polarization:
        plt.bar(list(dict_graphing.keys()), dict_graphing.values(), color='g')
        plt.title('RCV = First-Past-The-Post Primary Polarization')
        plt.show()
    else:
        plt.bar(list(dict_graphing.keys()), dict_graphing.values(), color='g')
        plt.title('RCV > First-Past-The-Post Primary Polarization')
        plt.show()

"""
This function generates the histogram for how voters rank their choices in the situation where RCV polarization > 
normal polarization.
"""
def make_hist_uniform_rcv_greater(num_candidates):
    candidates = gen_candidates_uniform(num_candidates)
    dict_graphing = generate_voter_choices_uniform(candidates)

    normal_system = find_normal_winner_uniform(candidates)
    RCV_system = find_RCV_winner_uniform(candidates)

    normal_polarization = normal_system[1]
    rcv_polarization = RCV_system[1]

    if rcv_polarization > normal_polarization:
        plt.bar(list(dict_graphing.keys()), dict_graphing.values(), color='g')
        plt.title('RCV > First-Past-The-Post Primary Polarization')
        plt.show()
    else:
        make_hist_uniform_rcv_greater(num_candidates)

"""
This function generates the histogram for how voters rank their choices in the situation where you choose the number of
left candidates.
"""
def make_hist_uniform_rcv_choose(num_candidates, num_left_candidates):
    candidates = gen_candidates_uniform(num_candidates)
    left_candidates = []
    for candidate in candidates:
        if candidate <= 10:
            left_candidates.append(candidate)
    if len(left_candidates) == num_left_candidates:
        dict_graphing = generate_voter_choices_uniform(candidates)

        plt.bar(list(dict_graphing.keys()), dict_graphing.values(), color='g')
        plt.title(str(num_left_candidates) + " left candidates")
        plt.show()
    else:
        make_hist_uniform_rcv_choose(num_candidates, num_left_candidates)

"""
This function graphs the scenarios where you can choose the number of left candidates in a scatter plot.
"""
def scatter_specific_uniform(num_candidates, num_run, num_left_candidates):
    x = []
    y = []

    for i in range(num_run):
        candidates = gen_candidates_uniform(num_candidates)
        left_candidates = []
        for j in range(len(candidates)):
            if candidates[j] <= 10:
                left_candidates.append(candidates[j])
        if len(left_candidates) == num_left_candidates:
            normal_system = find_normal_winner_uniform(candidates)
            RCV_system = find_RCV_winner_uniform(candidates)
            x.append(normal_system[1])
            y.append(RCV_system[1])

    plt.scatter(x, y, color="purple")

    plt.xlabel('Normal Election Polarization')
    plt.ylabel('Ranked Choice Voting Polarization')
    plt.title('RCV vs. First-Past-The-Post Primary Polarization')
    plt.show()

def print_candidates_RCV_greater_choose(num_candidates, num_left_candidates):
    candidates = gen_candidates_uniform(num_candidates)
    left_candidates = []
    for candidate in candidates:
        if candidate <= 10:
            left_candidates.append(candidate)
    if len(left_candidates) == num_left_candidates:
        dict_graphing = generate_voter_choices_uniform(candidates)
        normal_system = find_normal_winner_uniform(candidates)
        RCV_system = find_RCV_winner_uniform(candidates)

        normal_polarization = normal_system[1]
        rcv_polarization = RCV_system[1]

        if normal_polarization < rcv_polarization:
            print("The candidates in this election are " + str(candidates))
            plt.bar(list(dict_graphing.keys()), dict_graphing.values(), color='g')
            plt.title(str(num_left_candidates) + " left candidates")
            plt.show()
        else:
            print_candidates_RCV_greater_choose(num_candidates, num_left_candidates)
    else:
        print_candidates_RCV_greater_choose(num_candidates, num_left_candidates)

""" This function is a helper to plot a line based on slope and intercept"""
def abline(slope, intercept):
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

""" This function allows you to choose the winner of each election and compute the result. """
def choose_winners(num_candidates, num_run, num_left_candidates, winner_choice_CES, winner_choice_RCV):
    x = []
    y = []

    for i in range(num_run):
        candidates = gen_candidates_uniform(num_candidates)
        left_candidates = []

        for j in range(len(candidates)):
            if candidates[j] <= 10:
                left_candidates.append(candidates[j])
        if len(left_candidates) == num_left_candidates:
            CES_system = find_normal_winner_uniform(candidates)
            RCV_system = find_RCV_winner_uniform(candidates)
            CES_winner = CES_system[0]
            RCV_winner = RCV_system[0]

            if CES_winner == candidates[winner_choice_CES] and RCV_winner == candidates[winner_choice_RCV]:
                x.append(CES_system[1])
                y.append(RCV_system[1])

    plt.scatter(x, y, color="purple")
    plt.xlabel('Normal Election Polarization')
    plt.ylabel('Ranked Choice Voting Polarization')
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    abline(1, 0)
    plt.title('RCV vs. CES Polarization w/ ' + str(num_left_candidates) + 'left candidates, ' + str(winner_choice_CES)
              + 'CES winner, ' + str(winner_choice_RCV) + 'RCV_winner')
    plt.show()

def calculate_percent_uniform(num_candidates, num_run):
    RCV_winners = 0

    for i in range(num_run):
        candidates = gen_candidates_uniform(num_candidates)
        CES_system = find_normal_winner_uniform(candidates)
        RCV_system = find_RCV_winner_uniform(candidates)

        CES_polarization = CES_system[1]
        rcv_polarization = RCV_system[1]

        if rcv_polarization > CES_polarization:
            RCV_winners += 1

    total_percent = RCV_winners/num_run

    print("The percent of times that RCV performs worse is " + str(total_percent) + "%")
    return total_percent



def main():
    # First input is number of voters, second is number of candidates
    args = sys.argv[1:]
    if str(args[0]) == "uniform-once":
        """Run one election using a uniform distribution, where the first input is the number of candidates"""
        all_uniform_distribution(int(args[1]))
    elif str(args[0]) == "uniform-graph":
        """Create a scatter plot of the extremism in RCV vs CES, where the first input is the number of candidates
        and the second is the number of elections"""
        graph_uniform_results(int(args[1]), int(args[2]))
    elif str(args[0]) == "uniform-hist":
        """Create a histogram of voter's RCV rankings, given the number of candidates"""
        make_hist_uniform_rcv(int(args[1]))
    elif str(args[0]) == "scatter-specific-uniform":
        """Create a scatter plot of the extremism in RCV vs CES, where the first input is the number of candidates, the
        second is the number of elections, and the third is the number of left candidates"""
        scatter_specific_uniform(int(args[1]), int(args[2]), int(args[3]))
    elif str(args[0]) == "uniform-hist-rcv-greater":
        """Create a histogram of voter's RCV rankings in the scenario where RCV results in higher extremism, where the
        first input is the number of candidates"""
        make_hist_uniform_rcv_greater(int(args[1]))
    elif str(args[0]) == "uniform-hist-choose-left":
        """Create a histogram of voter's RCV rankings, where the first input is the number of candidates and the second
        is the number of left candidates"""
        make_hist_uniform_rcv_choose(int(args[1]), int(args[2]))
    elif str(args[0]) == "uniform-print-choose-greater":
        """Print the candidates in the case where RCV results in higher extremism than CES, where the first input is the
        number of candidates and the second is the number of left candidates"""
        print_candidates_RCV_greater_choose(int(args[1]), int(args[2]))
    elif str(args[0]) == "choose-winners":
        """Graph a scatter plot of the extremism in RCV vs CES, where the first input is the number of candidates,
        the second is the number of elections, the third is the number of left candidates, the fourth is the 
        index of the CES winner, and the fifth is the index of the RCV winner
        Note: index starts at 0, from left to right"""
        choose_winners(int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))
    elif str(args[0]) == "percents":
        """Print the percentage of times where RCV generates higher extremism than CES, where the first input is the
        number of candidates and the second is the number of elections"""
        calculate_percent_uniform(int(args[1]), int(args[2]))
    else:
        raise Exception("No option was selected")

if __name__ == '__main__':
    main()
