from scipy.interpolate import UnivariateSpline
from scipy.stats import norm, uniform
import matplotlib.pyplot as plt
import numpy as np
import random

RANDOMIZE_CANDIDATES = True
NUM_CANDIDATES = 4
leftCandidates = 2
rightCandidates = 2

TRIALS = 500000
TRIALS_PER_DISTRIBUTION = 10
NUM_GRAPH_SECTIONS = 50000000
NUM_SPLINE_SECTIONS = 10

GRAPH_SCALE = 1

def getVoterProportions(prefixSum, candidates):
    leftBound = 0
    proportions = []

    for i, candidate in enumerate(candidates):
        rightBound = round((candidate + candidates[i + 1]) / 2 if i != len(candidates) - 1 else len(prefixSum) - 1)
        proportions.append(prefixSum[rightBound] - prefixSum[leftBound])
        leftBound = rightBound + 1

    return proportions


def findSimpleElectionWinnerValue(prefixSum, candidates):
    proportions = np.array(getVoterProportions(prefixSum, candidates))
    return candidates[np.argmax(proportions)]


def findCESWinnerValue(prefixSum, medianLoc, candidates):
    winners = []
    if leftCandidates > 0:
        winners.append(findSimpleElectionWinnerValue(prefixSum[:medianLoc], candidates[:leftCandidates]))

    if rightCandidates > 0:
        winners.append(medianLoc + findSimpleElectionWinnerValue(prefixSum[medianLoc + 1:],
                                                         [candidate - medianLoc for candidate in candidates[leftCandidates:]]))

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


def randomSplineDistribution():
    xValues = np.linspace(0, 1, num=NUM_SPLINE_SECTIONS)
    yValues = np.random.rand(NUM_SPLINE_SECTIONS)
    return UnivariateSpline(xValues, yValues, k=4)

def randomNormalDistribution():
    return lambda distribution: norm.pdf(distribution, random.random() * 0.4)

def normalDistribution():
    return lambda distribution: norm.pdf(distribution, loc=0.5, scale=0.2)

def uniformDistribution():
    return lambda distribution: uniform.pdf(distribution)


def runGeneralDistributionVoters():
    global NUM_CANDIDATES, leftCandidates, rightCandidates

    CESPolarization = []
    RCVPolarization = []

    distribution = normalDistribution()
    # distribution = uniformDistribution()
    intervals = np.linspace(0, 1, num=NUM_GRAPH_SECTIONS)
    intervalHeights = distribution(intervals)

    prefixSum = np.append([0], np.cumsum(intervalHeights))
    medianLoc = np.searchsorted(prefixSum, prefixSum[-1] / 2)

    for trial in range(int(TRIALS / TRIALS_PER_DISTRIBUTION)):
        # distribution = randomNormalDistribution()
        # intervals = np.linspace(0, 1, num=NUM_GRAPH_SECTIONS)
        # intervalHeights = distribution(intervals)
        #
        # prefixSum = np.append([0], np.cumsum(intervalHeights))
        # medianLoc = np.searchsorted(prefixSum, prefixSum[-1] / 2)

        for trialDist in range(TRIALS_PER_DISTRIBUTION):
            # Ordered from left, moderate right, extreme right (index of candidates)
            candidates = []

            if RANDOMIZE_CANDIDATES:
                while len(candidates) < NUM_CANDIDATES:
                    randomCandidate = random.randrange(1, NUM_GRAPH_SECTIONS)
                    if randomCandidate != medianLoc:
                        candidates.append(randomCandidate)

                candidates.sort()

                # Count left and right candidates
                leftCandidates = 0
                rightCandidates = 0
                for candidate in candidates:
                    if candidate < medianLoc:
                        leftCandidates += 1
                    else:
                        rightCandidates += 1

            else:
                while len(candidates) < leftCandidates:
                    candidates.append(random.randrange(1, medianLoc))

                while len(candidates) < rightCandidates:
                    candidates.append(random.randrange(medianLoc + 1, NUM_GRAPH_SECTIONS))

                candidates.sort()

            CESWinner = findCESWinnerValue(prefixSum, medianLoc, candidates)
            RCVWinner = findRCVWinnerValue(prefixSum, candidates)

            CESPolarization.append(abs(CESWinner - medianLoc) * GRAPH_SCALE / NUM_GRAPH_SECTIONS)
            RCVPolarization.append(abs(RCVWinner - medianLoc) * GRAPH_SCALE / NUM_GRAPH_SECTIONS)

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

    print(f'Percentage of trials with better RCV Performance: {100 * float(numGreater)/len(CESPolarization)}')


runGeneralDistributionVoters()
