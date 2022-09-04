# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import math
from random import seed
from random import random
import statistics
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from collections import Counter

"""
Normal voting system first; then, RCV.
"""

"""
This function generates voters and candidates randomly, on a scale from 0 to 20, and returns
the sorted voters, median voter number, sorted candidates, and median candidate number.

It takes in the number of candidates and voters as variables.
"""
def generate_voters_candidates(num_voters, num_candidates):

    voters_original = []
    candidates_original = []
    for i in range(num_candidates):
        candidates_original.append(random() * 20)
    for i in range(num_voters):
        voters_original.append(random() * 20)
    voters_sorted = sorted(voters_original)
    candidates_sorted = sorted(candidates_original)
    median_voters = statistics.median(voters_sorted)
    median_candidates = statistics.median(candidates_sorted)
    return voters_sorted, median_voters, candidates_sorted, median_candidates

"""
 This code generates the winner in the left party in a primary system. It returns a list of
 all the winners. It takes in a list of all voters, the median voter, a list of all candidates, and the
 median candidate.
"""
def generate_winners_left(all_voters, median_voters, all_candidates, median_candidates):
    # Check to make sure that there will be a left primary

    counter = 0
    for i in range(len(all_candidates)):
        if all_candidates[i] > median_voters:
            counter += 1

    if counter == len(all_candidates):
        print("There is no left primary")
        return []

    left_voters = []
    for i in range(len(all_voters)):
        if all_voters[i] <= median_voters:
            left_voters.append(all_voters[i])
    left_candidates = []
    for i in range(len(all_candidates)):
        if all_candidates[i] <= median_voters:
            left_candidates.append(all_candidates[i])

    if len(left_candidates) == 1:
        print("The left primary winner is " + str(left_candidates))
        return left_candidates
    median_left_candidates = statistics.median(left_candidates)
    total_votes = {}
    median_left_voters = statistics.median(left_voters)

    for i in range(len(left_voters)):
        if left_voters[i] <= median_left_candidates:
            minimum = left_voters[i] - left_candidates[0]
            for j in range(len(left_candidates)):
                difference = abs(left_voters[i] - left_candidates[j])
                if difference <= minimum:
                    minimum = difference
                elif difference > minimum and left_candidates[j] != left_candidates[0]:
                    if left_candidates[j-1] not in total_votes:
                        total_votes[left_candidates[j - 1]] = 0
                    total_votes[left_candidates[j - 1]] += 1
                    break
                elif difference > minimum and left_candidates[j] == left_candidates[0]:
                    if left_candidates[j] not in total_votes:
                        total_votes[left_candidates[j]] = 0
                    total_votes[left_candidates[j]] += 1
                    break
        if left_voters[i] > median_left_candidates:
            minimum = left_voters[i] - left_candidates[len(left_candidates) - 1]
            for j in reversed(range(len(left_candidates))):
                difference = abs(left_voters[i] - left_candidates[j])
                if difference < minimum:
                    minimum = difference
                elif difference > minimum and left_candidates[j] != left_candidates[len(left_candidates) - 1]:
                    if left_candidates[j+1] not in total_votes:
                        total_votes[left_candidates[j + 1]] = 0
                    total_votes[left_candidates[j+1]] += 1
                    break
                elif difference > minimum and left_candidates[j] == left_candidates[len(left_candidates) - 1]:
                    if left_candidates[j] not in total_votes:
                        total_votes[left_candidates[j]] = 0
                    total_votes[left_candidates[j]] += 1
                    break
    winner_one = max(total_votes, key=total_votes.get)
    all_winners = []
    for key in total_votes.keys():
        if total_votes[key] == total_votes[winner_one]:
            all_winners.append(key)
    print("The Left Party Winner(s) is " + str(all_winners))
    return all_winners

"""
 This code generates the winner in the right party in a primary system. It returns a list of
 all the winners. It takes in a list of all voters, the median voter, a list of all candidates, and the
 median candidate.
"""
def generate_winners_right(all_voters, median_voters, all_candidates, median_candidates):
    # Check to make sure there is a right primary
    counter = 0

    for i in range(len(all_candidates)):
        if all_candidates[i] < median_voters:
            counter += 1

    if counter == len(all_candidates):
        print("There is no right primary")
        return []

    right_voters = []
    for i in range(len(all_voters)):
        if all_voters[i] > median_voters:
            right_voters.append(all_voters[i])
    total_votes = {}
    right_candidates = []
    for i in range(len(all_candidates)):
        if all_candidates[i] > median_voters:
            right_candidates.append(all_candidates[i])

    if len(right_candidates) == 1:
        print("The right primary winner is " + str(right_candidates))
        return right_candidates

    median_right_candidates = statistics.median(right_candidates)
    median_right_voters = statistics.median(right_voters)

    for i in range(len(right_voters)):
        if right_voters[i] <= median_right_candidates:
            minimum = right_voters[i] - right_candidates[0]
            for j in range(len(right_candidates)):
                difference = abs(right_voters[i] - right_candidates[j])
                if difference <= minimum:
                    minimum = difference
                elif difference > minimum and right_candidates[j] != right_candidates[0]:
                    if right_candidates[j-1] not in total_votes:
                        total_votes[right_candidates[j - 1]] = 0
                    total_votes[right_candidates[j - 1]] += 1
                    break
                elif difference > minimum and right_candidates[j] == right_candidates[0]:
                    if right_candidates[j] not in total_votes:
                        total_votes[right_candidates[j]] = 0
                    total_votes[right_candidates[j]] += 1
                    break
        if right_voters[i] > median_right_candidates:
            minimum = right_voters[i] - right_candidates[len(right_candidates) - 1]
            for j in reversed(range(len(right_candidates))):
                difference = abs(right_voters[i] - right_candidates[j])
                if difference < minimum:
                    minimum = difference
                elif difference > minimum and right_candidates[j] == right_candidates[len(right_candidates) - 1]:
                    if right_candidates[j] not in total_votes:
                        total_votes[right_candidates[j]] = 0
                    total_votes[right_candidates[j]] += 1
                    break
                elif difference > minimum and right_candidates[j] != right_candidates[len(right_candidates) - 1]:
                    if right_candidates[j+1] not in total_votes:
                        total_votes[right_candidates[j + 1]] = 0
                    total_votes[right_candidates[j+1]] += 1
                    break
    # print(total_votes)
    winner_one = max(total_votes, key=total_votes.get)
    all_winners = []
    for key in total_votes.keys():
        if total_votes[key] == total_votes[winner_one]:
            all_winners.append(key)
    print("The Right Party Winner(s) is " + str(all_winners))
    return all_winners

"""
This code takes inputs of the left winner, right winner, and all the voters, and return the ultimate winner and
polarization level in a  normal, first-past-the-post system. It prints the vote breakdown, ultimate winner, and 
polarization
"""
def ultimate_winner(left_winner, right_winner, all_voters):
    both_winners = [];
    total_votes = {}
    median_voter = statistics.median(all_voters)

    """
    Account for case where there is no left/right primary and there is an uncontested general
    """
    if not left_winner:
        print("All votes go to the right party-primary winner")
        print("The ultimate winner is "+ str(right_winner))
        polarization = abs(median_voter - right_winner[0])
        print("The polarization level for this election is " + str(polarization))
        return right_winner, polarization

    if not right_winner:
        print("All votes go to the left party-primary winner")
        print("The ultimate winner is " + str(left_winner))
        polarization = abs(median_voter - left_winner[0])
        print("The polarization level for this election is " + str(polarization))
        return left_winner, polarization

    for winner in left_winner:
        both_winners.append(winner)
    for winner in right_winner:
        both_winners.append(winner)
    median_candidates = statistics.median(both_winners)

    for i in range(len(all_voters)):
        if all_voters[i] <= median_candidates:
            minimum = all_voters[i] - both_winners[0]
            for j in range(len(both_winners)):
                difference = abs(all_voters[i] - both_winners[j])
                if difference <= minimum:
                    minimum = difference
                elif difference > minimum and both_winners[j] == both_winners[0]:
                    if both_winners[j] not in total_votes:
                        total_votes[both_winners[j]] = 0
                    total_votes[both_winners[j]] += 1
                    break
                elif difference > minimum and both_winners[j] != both_winners[0]:
                    if both_winners[j - 1] not in total_votes:
                        total_votes[both_winners[j - 1]] = 0
                    total_votes[both_winners[j - 1]] += 1
                    break
        if all_voters[i] > median_candidates:
            minimum = all_voters[i] - both_winners[len(both_winners) - 1]
            for j in reversed(range(len(both_winners))):
                difference = abs(all_voters[i] - both_winners[j])
                if difference < minimum:
                    minimum = difference
                elif difference > minimum and both_winners[j] != both_winners[len(both_winners) - 1]:
                    if both_winners[j + 1] not in total_votes:
                        total_votes[both_winners[j + 1]] = 0
                    total_votes[both_winners[j + 1]] += 1
                    break
                elif difference > minimum and both_winners[j] == both_winners[len(both_winners) - 1]:
                    if both_winners[j] not in total_votes:
                        total_votes[both_winners[j]] = 0
                    total_votes[both_winners[j]] += 1
                    break
    print("The ultimate Vote Breakdown is " + str(total_votes))

    winner_one = max(total_votes, key=total_votes.get)
    all_winners = []
    for key in total_votes.keys():
        if total_votes[key] == total_votes[winner_one]:
            all_winners.append(key)
    if len(all_winners) > 1:
        print("The result is a tie. The winners are " + str(all_winners))
        polarization = abs(median_voter - statistics.mean(all_winners))
    else:
        print("The ultimate winner is " + str(all_winners))
        polarization = abs(median_voter - all_winners[0])
        print("The polarization level for this election is " + str(polarization))

    return all_winners, polarization



"""
The code below takes inputs of the number of candidates and number of voters in the election, and finds the winner
based on a random distribution of candidates and voters.
This is a GENERAL example, and not directly run in main.
"""
def generate_winners_normal(num_candidates, num_voters):
    voters_original = []
    candidates_original = []
    for i in range(num_candidates):
        candidates_original.append(random()*20)
    for i in range(num_voters):
        voters_original.append(random() * 20)
    voters_sorted = sorted(voters_original)
    candidates_sorted = sorted(candidates_original)
    total_votes = {}
    median_voters = statistics.median(voters_sorted)
    median_candidates = statistics.median(candidates_sorted)

    for i in range(len(voters_sorted)):
        if voters_sorted[i] <= median_candidates:
            minimum = voters_sorted[i] - candidates_sorted[0]
            for j in range(len(candidates_sorted)):
                difference = abs(voters_sorted[i] - candidates_sorted[j])
                if difference <= minimum:
                    minimum = difference
                elif difference > minimum and candidates_sorted[j] != candidates_sorted[0]:
                    if candidates_sorted[j-1] not in total_votes:
                        total_votes[candidates_sorted[j - 1]] = 0
                    total_votes[candidates_sorted[j - 1]] += 1
                    break
                elif difference > minimum and candidates_sorted[j] == candidates_sorted[0]:
                    if candidates_sorted[j] not in total_votes:
                        total_votes[candidates_sorted[j]] = 0
                    total_votes[candidates_sorted[j]] += 1
                    break
        if voters_sorted[i] > median_candidates:
            minimum = voters_sorted[i] - candidates_sorted[len(candidates_sorted) - 1]
            for j in reversed(range(len(candidates_sorted))):
                difference = abs(voters_sorted[i] - candidates_sorted[j])
                if difference < minimum:
                    minimum = difference
                elif difference > minimum and candidates_sorted[j] != candidates_sorted[len(candidates_sorted) - 1]:
                    if candidates_sorted[j+1] not in total_votes:
                        total_votes[candidates_sorted[j + 1]] = 0
                    total_votes[candidates_sorted[j+1]] += 1
                    break
                elif difference > minimum and candidates_sorted[j] == candidates_sorted[len(candidates_sorted) - 1]:
                    if candidates_sorted[j] not in total_votes:
                        total_votes[candidates_sorted[j]] = 0
                    total_votes[candidates_sorted[j]] += 1
                    break
    print(total_votes)
    winner_one = max(total_votes, key=total_votes.get)
    all_winners = []
    for key in total_votes.keys():
        if total_votes[key] == total_votes[winner_one]:
            all_winners.append(key)
    print(all_winners)


"""
This is a helper that creates a sorted dictioonary
"""
def create_sorted_dict(dict):
    sorted_values = sorted(dict.values())  # Sort the values
    sorted_dict = {}
    for i in sorted_values:
        for k in dict.keys():
            if dict[k] == i:
                sorted_dict[k] = dict[k]
                break
    return sorted_dict

"""
This is a helper that returns the keys of a dictionary as a list
"""
def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list

""" 
This function creates the votes for ranked choice voting as a list, taking in the voters and candidates.
"""
def create_rcv_votes(all_voters_rcv, all_candidates_rcv):
    ranked_votes = []
    # have voters_sorted from generate voters function
    for i in range(len(all_voters_rcv)):
        candidate_distance = {}
        for j in range(len(all_candidates_rcv)):
            distance = abs(all_voters_rcv[i] - all_candidates_rcv[j])
            candidate_distance[all_candidates_rcv[j]] = distance
        #sorted_distances = sorted(candidate_distance.values())
        # Need to create the same dictionary, sorted by values, and add the keys to a list
        sorted_distances = create_sorted_dict(candidate_distance)
        keys = getList(sorted_distances)
        ranked_votes.append(keys)
    return ranked_votes

"""
This function creates the winner for RCV, taking in the votes and the median voters
"""
def create_rcv_winner(ranked_votes, median_voters):
    eliminated_candidates = []
    half_voters = len(ranked_votes) / 2
    while True:
        first_choice_tally = {}
        for choices in ranked_votes:
            for choice in choices:
                if choice not in eliminated_candidates:
                    if choice not in first_choice_tally:
                        first_choice_tally[choice] = 0
                    first_choice_tally[choice] += 1
                    break

        for top_candidate in first_choice_tally:
            if first_choice_tally[top_candidate] > half_voters:
                print("The first choice vote breakdown is " + str(first_choice_tally))
                print("The winning ranked choice candidate is " + str(top_candidate))
                polarization = abs(top_candidate - median_voters)
                print("The polarization level is " + str(polarization))
                return top_candidate, polarization
        least_votes = min(first_choice_tally, key=first_choice_tally.get)
        eliminated_candidates.append(least_votes)

"""
This function combines the other functions to print the candidates, the winners in the primary system,
and the winners in the RCV system.
"""
def all_functions(num_voters, num_candidates):
    result = generate_voters_candidates(num_voters, num_candidates)

    print("The candidates in this election are " + str(result[2]))
    print("")
    print("In a typical, plurality, primary system:")
    left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
    right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
    ultimate_winner(left_winner, right_winner, result[0])
    print("")
    print("In a ranked choice, voting system:")
    voter_choices = create_rcv_votes(result[0], result[2])
    create_rcv_winner(voter_choices, result[1])

"""
This function graphs the results of polarization in a scatterplot.
"""
def graph_results(num_voters, num_candidates, num_run):
    x = []
    y = []

    for i in range(num_run):
        result = generate_voters_candidates(num_voters, num_candidates)
        left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
        right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
        normal_result = ultimate_winner(left_winner, right_winner, result[0])

        voter_choices = create_rcv_votes(result[0], result[2])
        rcv_result = create_rcv_winner(voter_choices, result[1])
        x.append(normal_result[1])
        y.append(rcv_result[1])

    plt.scatter(x, y,  color="purple")

    # x-axis label
    plt.xlabel('Normal Election Polarization')
    # frequency label
    plt.ylabel('Ranked Choice Voting Polarization')
    # plot title
    plt.title('RCV vs. First-Past-The-Post Primary Polarization')
    # showing legend

    # function to show the plot
    plt.show()

"""
This function prints the candidate and voter distributions for an example election.
"""
def find_distributions_for_point(num_voters, num_candidates):
    result = generate_voters_candidates(num_voters, num_candidates)

    print("The candidates in this election are " + str(result[2]))
    print("")
    print("In a typical, plurality, primary system:")
    left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
    right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
    ultimate_winner(left_winner, right_winner, result[0])
    print("")
    print("In a ranked choice, voting system:")
    voter_choices = create_rcv_votes(result[0], result[2])
    create_rcv_winner(voter_choices, result[1])

    print("The voter distribution is " + str(result[0]))

"""
This function makes a histogram of the RCV outcome. The bars are the candidate rankings for each voter.
"""
def make_histogram_RCV(num_voters, num_candidates):
    result = generate_voters_candidates(num_voters, num_candidates)
    left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
    right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
    normal_result = ultimate_winner(left_winner, right_winner, result[0])
    candidates = result[2]

    voter_choices = create_rcv_votes(result[0], result[2])
    rcv_result = create_rcv_winner(voter_choices, result[1])

    normal_polarization = normal_result[1]
    rcv_polarization = rcv_result[1]

    dict_graphing = {}
    for vote in voter_choices:
        new_vote = str(round(vote[0], 2)) + " " + str(round(vote[1], 2)) + " " + str(round(vote[2], 2))
        if new_vote not in dict_graphing:
            dict_graphing[new_vote] = 0
        dict_graphing[new_vote] += 1

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
This function is similar to the function that generates a scatterplot of polarization levels, but more specific.
You can input the # of voters, # candidates, # elections simulated, and # left candidates, and see the resulting graph.
In other words, you can specify the distribution of candidates (how many left candidates, how many right candidates 
there are) and see the result.
"""
def graph_specific_polarization(num_voters, num_candidates, num_run, num_left_candidates):
    x = []
    y = []

    for i in range(num_run):
        result = generate_voters_candidates(num_voters, num_candidates)
        candidates = result[2]
        left_candidates = []
        for j in range(len(candidates)):
            if candidates[j] <= result[1]:
                left_candidates.append(candidates[j])
        if len(left_candidates) == num_left_candidates:
            left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
            right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
            normal_result = ultimate_winner(left_winner, right_winner, result[0])

            voter_choices = create_rcv_votes(result[0], result[2])
            rcv_result = create_rcv_winner(voter_choices, result[1])
            x.append(normal_result[1])
            y.append(rcv_result[1])

    plt.scatter(x, y, color="purple")

    # x-axis label
    plt.xlabel('Normal Election Polarization')
    # frequency label
    plt.ylabel('Ranked Choice Voting Polarization')
    # plot title
    plt.title('RCV vs. Normal Polarization with ' + str(num_left_candidates) + ' left candidates and ' +
              str(num_candidates) + ' candidates')
    # showing legend

    # function to show the plot
    plt.show()

"""
This function reports the number of situations, given a number of times the program is run, that RCV
polarization > normal polarization, that RCV polarization < normal polarization, and that RCV polarization = normal 
polarization
"""
def report_percentages(num_voters, num_candidates, num_run):
    percentages = {}

    for i in range(num_run):
        result = generate_voters_candidates(num_voters, num_candidates)
        left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
        right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
        normal_result = ultimate_winner(left_winner, right_winner, result[0])

        voter_choices = create_rcv_votes(result[0], result[2])
        rcv_result = create_rcv_winner(voter_choices, result[1])

        if rcv_result[1] > normal_result[1]:
            if "RCV > normal" not in percentages:
                percentages["RCV > normal"] = 0
            percentages["RCV > normal"] += 1
        elif rcv_result[1] == normal_result[1]:
            if "RCV = normal" not in percentages:
                percentages["RCV = normal"] = 0
            percentages["RCV = normal"] += 1
        else:
            if "RCV < normal" not in percentages:
                percentages["RCV < normal"] = 0
            percentages["RCV < normal"] += 1

    print(percentages)


"""
This function prints the candidate distribution for a scenario where RCV polarization > normal election polarization
"""
def find_candidates_for_RCV_greater(num_voters, num_candidates):
    result = generate_voters_candidates(num_voters, num_candidates)

    left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
    right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
    normal_result = ultimate_winner(left_winner, right_winner, result[0])
    voter_choices = create_rcv_votes(result[0], result[2])
    rcv_result = create_rcv_winner(voter_choices, result[1])

    if rcv_result[1] <= normal_result[1]:
        find_candidates_for_RCV_greater(num_voters, num_candidates)
    else:
        print(" ")
        print("The candidates in this election are " + str(result[2]))

def find_voters_candidates_for_RCV_greater(num_voters, num_candidates):
    sys.setrecursionlimit(10000)
    result = generate_voters_candidates(num_voters, num_candidates)

    left_winner = generate_winners_left(result[0], result[1], result[2], result[3])
    right_winner = generate_winners_right(result[0], result[1], result[2], result[3])
    normal_result = ultimate_winner(left_winner, right_winner, result[0])
    voter_choices = create_rcv_votes(result[0], result[2])
    rcv_result = create_rcv_winner(voter_choices, result[1])

    num_election_winners = len(normal_result[0])

    if rcv_result[1] <= normal_result[1]:
        find_voters_candidates_for_RCV_greater(num_voters, num_candidates)
    elif num_election_winners > 1:
        find_voters_candidates_for_RCV_greater(num_voters, num_candidates)
    else:
        print(" ")
        print("The voters in this election are " + str(result[0]))
        print(" ")
        print("The candidates in this election are " + str(result[2]))
"""
This function generates a given number of candidates randomly.
"""
def gen_candidates_uniform(num_candidates):
    # generate candidates
    candidates_original = []
    for i in range(num_candidates):
        candidates_original.append(random() * 20)
    candidates_sorted = sorted(candidates_original)
    print("The candidates are " + str(candidates_sorted))
    print("")
    return candidates_sorted

"""
Given a list of candidates, this function recursively generates the RCV winner and polarization level.
"""
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

"""
This function just generates the R1 RCV votes for the histogram.
"""
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
    # goal: generate dictionary, keys are the candidate combinations, values are the proportion that they occur
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


"""
This function generates the normal system (primary, general election) winner and polarization level, given
a list of candidates
"""
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

    # x-axis label
    plt.xlabel('Normal Election Polarization')
    # frequency label
    plt.ylabel('Ranked Choice Voting Polarization')
    # plot title
    plt.title('RCV vs. First-Past-The-Post Primary Polarization')
    # showing legend

    # function to show the plot
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
This function generates the histogram for how voters rank their choices in the situation where you choose the number of left candidates.
"""
def make_hist_uniform_rcv_choose(num_candidates, num_left_candidates):
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

        plt.bar(list(dict_graphing.keys()), dict_graphing.values(), color='g')
        plt.title(str(num_left_candidates) + " left candidates")
        plt.show()
    else:
        make_hist_uniform_rcv_choose(num_candidates, num_left_candidates)

"""
This function graphs the scenarios where you can choose the number of left candidates.
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

    # x-axis label
    plt.xlabel('Normal Election Polarization')
    # frequency label
    plt.ylabel('Ranked Choice Voting Polarization')
    # plot title
    plt.title('RCV vs. First-Past-The-Post Primary Polarization')
    # showing legend

    # function to show the plot
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

# Helper to plot a line based on slope and intercent
def abline(slope, intercept):
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')
"""
This function allows you to choose the winner of each election and compute the result.
"""
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

    # x-axis label
    plt.xlabel('Normal Election Polarization')
    # frequency label
    plt.ylabel('Ranked Choice Voting Polarization')
    # plot title
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    abline(1, 0)
    plt.title('RCV vs. CES Polarization w/ ' + str(num_left_candidates) + 'left candidates, ' + str(winner_choice_CES) + 'CES winner, ' + str(winner_choice_RCV) + 'RCV_winner')
    # showing legend

    # function to show the plot
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
    if str(args[0]) == "once": # Run it once
        all_functions(int(args[1]), int(args[2]))
    elif str(args[0]) == "identify": # print winners and distributions of voters/candidates
            find_distributions_for_point(int(args[1]), int(args[2]))
    elif str(args[0]) == "hist":
        make_histogram_RCV(int(args[1]), int(args[2])) #num voters, num candidates
    elif str(args[0]) == "specific":
        graph_specific_polarization(int(args[1]), int(args[2]), int(args[3]), int(args[4]))
        #num_voters, num_candidates, num_run, num_left_candidates
    elif str(args[0]) == "percentages":
        report_percentages(int(args[1]), int(args[2]), int(args[3]))
        # num voters, num candidates, num run
    elif str(args[0]) == "candidates-specific":
        find_candidates_for_RCV_greater(int(args[1]), int(args[2]))
        # num voters, num candidates
    elif str(args[0]) == "uniform-once":
        all_uniform_distribution(int(args[1]))
        # num candidates
    elif str(args[0]) == "uniform-graph":
        graph_uniform_results(int(args[1]), int(args[2]))
        # num candidates, num run
        # creates scatterplot of polarizations with uniform distribution
    elif str(args[0]) == "uniform-hist":
        make_hist_uniform_rcv(int(args[1]))
        # num candidates
        # creates hist of proportions of rankings
    elif str(args[0]) == "scatter-specific-uniform":
        scatter_specific_uniform(int(args[1]), int(args[2]), int(args[3]))
        # num candidates, num run, num left candidates
        # produces scatterplot, but you specify the nunber of left candidates
    elif str(args[0]) == "uniform-hist-rcv-greater":
        make_hist_uniform_rcv_greater(int(args[1]))
        # num candidates
        # creates hist of proportion of rankings in scenario where RCV polarization greater
    elif str(args[0]) == "uniform-hist-choose-left":
        make_hist_uniform_rcv_choose(int(args[1]), int(args[2]))
        # num_candidates, then num left candidates
        # Creates hist of proportion of rankings in scenario where you choose num left candidates
    elif str(args[0]) == "uniform-print-choose-greater":
        # num candidates, then num left candidates
        # prints candidates in case where RCV polarization > normal election, given # of left candidates
        print_candidates_RCV_greater_choose(int(args[1]), int(args[2]))
    elif str(args[0]) == "voters-specific":
        # returns voters and candidates in scenario where RCV polarization > normal
        find_voters_candidates_for_RCV_greater(int(args[1]), int(args[2]))
        # num voters, num candidates
    elif str(args[0]) == "choose-winners":
        # Returns scatterplot in scenario where you choose which candidate wins and num left candidates
        # Num candidates, num run, num left candidates, winner_choice_CES, winner_choice_RCV
        # winner choice CES starts at 0, represents where the candidates is (e.g. 0 means most far left candidate)
        choose_winners(int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))
    elif str(args[0]) == "percents":
        # Prints percent of times RCV does worse
        # num candidates, num run
        calculate_percent_uniform(int(args[1]), int(args[2]))
    else: # Simulate a bunch, graph
        graph_results(int(args[0]), int(args[1]), int(args[2])) #num voters, num candidates, num run



if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""
 # ranked_votes.append([])
           # if all_voters_rcv[i] <= median_candidates:
               # minimum = all_voters_rcv[i] - all_candidates_rcv[0]
                for j in range(len(all_candidates_rcv)):
                    difference = abs(all_voters_rcv[i] - all_candidates_rcv[j])
                    if difference <= minimum:
                        minimum = difference
                    elif difference > minimum and all_candidates_rcv[j] != all_candidates_rcv[0]:
                        individual_rankings = ranked_votes[i]
                        individual_rankings.append(all_candidates_rcv[j-1])

                        if abs(all_voters_rcv[i] - all_candidates_rcv[j]) < abs(all_voters_rcv[i] - all_candidates_rcv[j-2]):
                            individual_rankings.append(all_candidates_rcv[j])
                            if abs(all_voters_rcv[i] - all_candidates_rcv[j-2]) < abs(all_voters_rcv[i] - all_candidates_rcv[j+1]):
                                individual_rankings.append(all_candidates_rcv[j-2])
                                if abs(all_voters_rcv[i] - all_candidates_rcv[])
                    elif difference > minimum and all_candidatesrcv[j] == all_candidates_rcv[0]:
                        individual_rankings.append(all_candidates_rcv[j])
                all_candidates_edited = all_candidates_rcv.remove(individual_rankings[i][0])
RCV Plan:
1. Repeat same thing as in the past to generate first choice votes
2. Repeat but for second choice votes, do i - 2 instead, compare to i + 1, see which one is smaller, do that (make 
second choice dictionary too)
- make sure to account for edge cases/when there is no i-2, etc. (like if at high end, it'll rank the closest, then
second highest, then third highest, etc.; if at low end, it'll rank lowest, then second lwoest, then third, etc.)
3. Repeat for third, fourth, fifth choices
this will give 5 dictionaries with first, second, third, fourth, fifth ranked candidates, with the # votes of each

Now it's time to generate the winner:
make a function that generates winner
- if the number of first choice votes that the winner has >= 50%: return that winner; print the winner and polarization level
- else:
    1. find candidate with fewest first choice votes
    2. 
    3. 
Alternative:
Loop through voters
Make dictionary for each voter
each_voters_votes[voter] = [1st choice, 2nd choice, third,...]
- find 1st, 2nd, 3rd normal way
winners dictionary which is the same as last

Loop through the each_voters_votes dictionary (loop through the keys)
- winners

Now it's time to generate the winner:
- if 

Updated Plan with Rohan:

MAKE A dictionary of distances to candidates
sort it
then find candidates w shortest distances
add to candidates list

do the winner stuff from that for each voter since each voter has a list

Ultimate:
First function, creating the votes
Create a list of lists called ranked _votes
Each voter will have a list within ranked_votes, representing their first, second, third...fifth choice candidate
So for each voter, loop through and find their respective winners, add to the list in order
Return ranked_votes

Make A dictionary of distances to candidates (defined IN the voter loop)
- Each voter has one
- make key the candidate #, value the distance
- sort this (value in increasing order)
- Turn the keys into a list, and add that list to the ranked_votes list

Then, second function:
Initialize eliminated_candidates list
while true:
Loop through ranked_votes:
- Take the first value in each list that is NOT in eliminated candidates
, tally up votes in a dictionary called first_choice_tally

Loop through candidates:
- if first_choice_tally[candidate]/#ofvoters >= 0.5:
    return and print that candidate
    find polarization level, print that
    break

else:
- find the min of the first choice tallies
- add that candidate to eliminate candidates list
"""