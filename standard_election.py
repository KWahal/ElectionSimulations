"""
This file allows you to choose the number of voters and candidates in an election, and randomly generates the voters
and candidates. It then calculates the winner of the election under a primary system and under ranked-choice voting. as
well as the extremism levels of the winning candidates.

It provides the option to provide a variety of visualizations, such as the proportion of voters that hold a particular
ranking system for candidates and scatter plots comparing the extremism levels for the two types of elections.
If you choose, it is relatively easy to modify this code such that you manually decide the candidates or voters.

This simulation code is based on a discrete number of voters.
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
This function generates the winner in the left party in a primary system. It returns a list of
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
 This function generates the winner in the right party in a primary system. It returns a list of
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
    winner_one = max(total_votes, key=total_votes.get)
    all_winners = []
    for key in total_votes.keys():
        if total_votes[key] == total_votes[winner_one]:
            all_winners.append(key)
    print("The Right Party Winner(s) is " + str(all_winners))
    return all_winners

"""
This function takes inputs of the left winner, right winner, and all the voters, and return the ultimate winner and
polarization level in a  normal, first-past-the-post system. It prints the vote breakdown, ultimate winner, and 
polarization
"""
def ultimate_winner(left_winner, right_winner, all_voters):
    both_winners = [];
    total_votes = {}
    median_voter = statistics.median(all_voters)

    """ Account for case where there is no left/right primary and there is an uncontested general """
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
This function takes inputs of the number of candidates and number of voters in the election, and finds the winner
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
This is a helper that creates a sorted dictionary
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
This function graphs the results of extremism in a scatterplot.
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
    plt.xlabel('Normal Election Polarization')
    plt.ylabel('Ranked Choice Voting Polarization')
    plt.title('RCV vs. First-Past-The-Post Primary Polarization')
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
    plt.xlabel('Normal Election Polarization')
    plt.ylabel('Ranked Choice Voting Polarization')
    plt.title('RCV vs. Normal Polarization with ' + str(num_left_candidates) + ' left candidates and ' +
              str(num_candidates) + ' candidates')
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
This function prints the voter and candidate distribution for a scenario where RCV polarization > normal election polarization
"""
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


def main():
    args = sys.argv[1:]
    if str(args[0]) == "once":
        """Run one election, where the first input is the number of voters, the second is the number of candidates"""
        all_functions(int(args[1]), int(args[2]))
    elif str(args[0]) == "identify": # print winners and distributions of voters/candidates
        """Print the winners and distributions of voters/candidates for a single election, where the first input is
        the number of voters and the second is the number of candidates"""
        find_distributions_for_point(int(args[1]), int(args[2]))
    elif str(args[0]) == "hist":
        """Create a histogram of voter RCV rankings, where the first input is the number of voters, and the
        second is the number of candidates """
        make_histogram_RCV(int(args[1]), int(args[2]))
    elif str(args[0]) == "specific":
        """Graph a scatter plot documenting the extremism of the winning candidate in RCV vs CES, where the first input
        is the number of voters, the second is the number of candidates, the third is the number of elections run, and
        the fourth is the number of left candidates"""
        graph_specific_polarization(int(args[1]), int(args[2]), int(args[3]), int(args[4]))
    elif str(args[0]) == "percentages":
        """Print the percentage of times where RCV generates higher extremism than CES. The first input is the number
        of voters, the second is the number of candidates, and the third is the number of elections run."""
        report_percentages(int(args[1]), int(args[2]), int(args[3]))
    elif str(args[0]) == "voters-specific":
        """Print the voter and candidate distribution in the case where RCV generates higher extremism than CES.
        The first input is the number of voters, the second is the number of candidates."""
        find_voters_candidates_for_RCV_greater(int(args[1]), int(args[2]))
    elif str(args[0]) == "scatterplot":
        """Graph a scatter plot documenting the extremism of the winning candidate in RCV vs CES, where the first input
        is the number of voters, the second is the number of candidates, and the third is the number of elections run"""
        graph_results(int(args[0]), int(args[1]), int(args[2]))
    else:
        raise Exception("No option was selected")



if __name__ == '__main__':
    main()