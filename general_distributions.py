import math

from scipy.interpolate import UnivariateSpline
from scipy.stats import norm, uniform
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
import copy

RANDOMIZE_CANDIDATES = True
NUM_CANDIDATES = 4
LEFT_CANDIDATES = 2
RIGHT_CANDIDATES = 2

NUM_GRAPH_SECTIONS = 5000000
NUM_SPLINE_SECTIONS = 10

GRAPH_SCALE = 1


def getVoterProportions(prefixSum, candidates, leftBound=None, maxRightBound=None):
    # Setup leftBound + maxRightBound if necessary
    if maxRightBound == None:
        maxRightBound = len(prefixSum)
    
    if leftBound == None:
        leftBound = 0

    proportions = []

    for i, candidate in enumerate(candidates):
        rightBound = round(((candidate + candidates[i + 1]) / 2)
                           if (i != len(candidates) - 1) else (len(prefixSum) - 1))
        rightBound = min(rightBound, maxRightBound)

        if rightBound > leftBound:
            proportions.append(prefixSum[rightBound] - prefixSum[leftBound])
        else:
            proportions.append(0)
        
        leftBound = max(leftBound, rightBound)

    return proportions


def findSimpleElectionWinnerValue(prefixSum, candidates, leftBound=None, maxRightBound=None):
    proportions = np.array(getVoterProportions(prefixSum, candidates, leftBound=leftBound, maxRightBound=maxRightBound))
    return candidates[np.argmax(proportions)]


def findCESWinnerValue(prefixSum, indiffLoc, candidates, leftCandidates, rightCandidates, leftBound=None, maxRightBound=None):
    if leftBound == None:
        leftBound = indiffLoc
    
    if maxRightBound == None:
        maxRightBound = indiffLoc

    winners = []
    if leftCandidates > 0:
        winners.append(findSimpleElectionWinnerValue(prefixSum[:indiffLoc], candidates[:leftCandidates],
                                                     maxRightBound=maxRightBound))

    if rightCandidates > 0:
        winners.append(indiffLoc + findSimpleElectionWinnerValue(prefixSum[indiffLoc:],
                                                                 [candidate - indiffLoc for candidate in candidates[leftCandidates:]],
                                                                 leftBound=leftBound - indiffLoc))

    if len(winners) == 1:
        return winners[0]

    proportions = getVoterProportions(prefixSum, winners)

    return winners[0] if proportions[0] >= proportions[1] else winners[1]


def findRCVWinnerValue(prefixSum, candidates):
    if len(candidates) == 1:
        return candidates[0]

    proportions = np.array(getVoterProportions(prefixSum, candidates))

    # Remove lowest candidate
    del candidates[np.argmin(proportions)]
    return findRCVWinnerValue(prefixSum, candidates)

def findAlaskaWinnerValue(prefixSum, candidates):
    if len(candidates) == 1:
        return candidates[0]

    proportions = np.array(getVoterProportions(prefixSum, candidates))
    num_top_candidates = min(4, len(candidates))  # Ensure we don't exceed the number of candidates

    top_candidate_inds = np.argsort(proportions)[-num_top_candidates:]
    top_candidates = [candidates[i] for i in top_candidate_inds]
    top_candidates.sort()
    
    return findRCVWinnerValue(prefixSum, top_candidates)

def findNYCWinnerValue(prefixSum, indiffLoc, candidates, leftCandidates, rightCandidates):
    winners = []

    if leftCandidates > 0:
        winners.append(findRCVWinnerValue(prefixSum[:indiffLoc], candidates[:leftCandidates]))

    if rightCandidates > 0:
        winners.append(indiffLoc + findRCVWinnerValue(prefixSum[indiffLoc:],
                                                      [candidate - indiffLoc for candidate in candidates[leftCandidates:]]))

    if len(winners) == 1:
        return winners[0]

    proportions = getVoterProportions(prefixSum, winners)

    return winners[0] if proportions[0] >= proportions[1] else winners[1]


def randomSplineDistribution():
    xValues = np.linspace(0, 1, num=NUM_SPLINE_SECTIONS)
    yValues = np.random.rand(NUM_SPLINE_SECTIONS)
    return UnivariateSpline(xValues, yValues, k=5)


def randomNormalDistribution():
    return lambda distribution: norm.pdf(distribution, random.random() * 0.4)


def normalDistribution(dLoc=0.5, dScale=0.2):
    return lambda distribution: norm.pdf(distribution, loc=dLoc, scale=dScale)


def uniformDistribution():
    return lambda distribution: uniform.pdf(distribution)


def runGeneralDistributionVoters(loc=0.5, scale=0.2, trials=500000, tilt=0.5, graphSections=NUM_GRAPH_SECTIONS,
                                 numCandidates=NUM_CANDIDATES, randomizeCandidates=RANDOMIZE_CANDIDATES,
                                 leftCandidates=LEFT_CANDIDATES, rightCandidates=RIGHT_CANDIDATES, isNormal=True,
                                 distributionToUse=normalDistribution, recreateDistribution=False, trialsPerRecreation=100,
                                 runOtherVotingMethods=False, runClosed=False, independentRegions=(0.5, 0.5)):
    # Don't use other voting methods + closed election at the same time
    assert(not (runOtherVotingMethods and runClosed))
    
    CESPolarization = []
    RCVPolarization = []

    if runOtherVotingMethods:
        alaskaPolarization = []
        NYCPolarization = []
    elif runClosed:
        CESClosedPolarization = []

    if isNormal:
        distribution = distributionToUse(dLoc=loc, dScale=scale)
    else:
        distribution = distributionToUse()

    intervals = np.linspace(0, 1, num=graphSections)
    intervalHeights = distribution(intervals)

    prefixSum = np.append([0], np.cumsum(intervalHeights))

    if runClosed:
        maxRightBound = np.searchsorted(prefixSum, prefixSum[-1] * independentRegions[0])
        leftBound = np.searchsorted(prefixSum, prefixSum[-1] * independentRegions[1])

    # Location of the indifferent voter
    indiffLoc = np.searchsorted(prefixSum, prefixSum[-1] * tilt)
    medianLoc = np.searchsorted(prefixSum, prefixSum[-1] / 2)

    for trial in range(trials):
        # Recreate distribution if necessary
        if recreateDistribution and trial % trialsPerRecreation == 0:
            distribution = distributionToUse()
            intervalHeights = distribution(intervals)

            prefixSum = np.append([0], np.cumsum(intervalHeights))

            # Tilt represents district tilt (0.5 is median)
            indiffLoc = np.searchsorted(prefixSum, prefixSum[-1] * tilt)
            medianLoc = np.searchsorted(prefixSum, prefixSum[-1] / 2)

        # Sorted list of candidates
        candidates = []

        if randomizeCandidates:
            # Randomly pick candidates from voter distribution
            while len(candidates) < numCandidates:
                randomCandidate = random.randint(0, math.floor(prefixSum[-1]) * 5000) / 5000.
                candidateLocation = np.searchsorted(prefixSum, randomCandidate)

                if candidateLocation != indiffLoc:
                    candidates.append(candidateLocation)

            candidates.sort()

            # Count left and right candidates
            leftCandidates = 0
            rightCandidates = 0
            for candidate in candidates:
                if candidate < indiffLoc:
                    leftCandidates += 1
                else:
                    rightCandidates += 1
        else:
            # Generate random left candidates
            while len(candidates) < leftCandidates:
                candidates.append(random.randrange(1, indiffLoc))

            # Generate random right candidates
            while len(candidates) < rightCandidates:
                candidates.append(random.randrange(indiffLoc + 1, graphSections))

            candidates.sort()

        # Find election winners
        CESWinner = findCESWinnerValue(prefixSum, indiffLoc, candidates, leftCandidates, rightCandidates)
        RCVWinner = findRCVWinnerValue(prefixSum, copy.copy(candidates))

        CESPolarization.append(abs(CESWinner - medianLoc) * GRAPH_SCALE / graphSections)
        RCVPolarization.append(abs(RCVWinner - medianLoc) * GRAPH_SCALE / graphSections)

        if runOtherVotingMethods:
            alaskaWinner = findAlaskaWinnerValue(prefixSum, candidates)
            NYCWinner = findNYCWinnerValue(prefixSum, indiffLoc, candidates, leftCandidates, rightCandidates)

            alaskaPolarization.append(abs(alaskaWinner - medianLoc) * GRAPH_SCALE / graphSections)
            NYCPolarization.append(abs(NYCWinner - medianLoc) * GRAPH_SCALE / graphSections)
        elif runClosed:
            CESClosedWinner = findCESWinnerValue(prefixSum, indiffLoc, candidates, leftCandidates, rightCandidates, leftBound=leftBound, maxRightBound=maxRightBound)
            CESClosedPolarization.append(abs(CESClosedWinner - medianLoc) * GRAPH_SCALE / graphSections)

    if runOtherVotingMethods:
        return CESPolarization, RCVPolarization, alaskaPolarization, NYCPolarization
    elif runClosed:
        return CESPolarization, RCVPolarization, CESClosedPolarization
    
    return CESPolarization, RCVPolarization


def runAndShowGeneralDistributionVoters(nLoc=0.5, nScale=0.2, nTrials=500000):
    CESPolarization, RCVPolarization = runGeneralDistributionVoters(loc=nLoc, scale=nScale, trials=nTrials)

    # x-axis label
    plt.xlabel('Current Election System Polarization')
    # frequency label
    plt.ylabel('Ranked Choice Voting Polarization')
    # plot title
    plt.title(f'RCV vs. CES Polarization with {NUM_CANDIDATES} Candidates')

    numGreater = 0
    for i, CESPol in enumerate(CESPolarization):
        if RCVPolarization[i] <= CESPol:
            numGreater += 1

    plt.scatter(CESPolarization, RCVPolarization, color='purple')
    plt.show()

    print(f'Percentage of trials with better RCV Performance: {100 * float(numGreater) / len(CESPolarization)}')


runAndShowGeneralDistributionVoters(nLoc=0.5, nScale=0.2, nTrials=10000)
