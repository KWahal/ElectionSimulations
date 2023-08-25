import math

from scipy.interpolate import UnivariateSpline
from scipy.stats import norm, uniform
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm

RANDOMIZE_CANDIDATES = True
NUM_CANDIDATES = 4
LEFT_CANDIDATES = 2
RIGHT_CANDIDATES = 2

NUM_GRAPH_SECTIONS = 5000000
NUM_SPLINE_SECTIONS = 10

GRAPH_SCALE = 1


def getVoterProportions(prefixSum, candidates):
    leftBound = 0
    proportions = []

    for i, candidate in enumerate(candidates):
        rightBound = round((candidate + candidates[i + 1]) / 2
                           if i != len(candidates) - 1 else len(prefixSum) - 1)
        proportions.append(prefixSum[rightBound] - prefixSum[leftBound])
        leftBound = rightBound + 1

    return proportions


def findSimpleElectionWinnerValue(prefixSum, candidates):
    proportions = np.array(getVoterProportions(prefixSum, candidates))
    return candidates[np.argmax(proportions)]


def findCESWinnerValue(prefixSum, medianLoc, candidates, leftCandidates, rightCandidates):
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
    return UnivariateSpline(xValues, yValues, k=5)


def randomNormalDistribution():
    return lambda distribution: norm.pdf(distribution, random.random() * 0.4)


def normalDistribution(dLoc=0.5, dScale=0.2):
    return lambda distribution: norm.pdf(distribution, loc=dLoc, scale=dScale)


def uniformDistribution():
    return lambda distribution: uniform.pdf(distribution)


def runGeneralDistributionVoters(loc=0.5, scale=0.2, trials=500000, graphSections=NUM_GRAPH_SECTIONS,
                                 numCandidates=NUM_CANDIDATES, randomizeCandidates=RANDOMIZE_CANDIDATES,
                                 leftCandidates=LEFT_CANDIDATES, rightCandidates=RIGHT_CANDIDATES, isNormal=True,
                                 distributionToUse=normalDistribution, recreateDistribution=False, trialsPerRecreation=100):
    CESPolarization = []
    RCVPolarization = []

    if isNormal:
        distribution = distributionToUse(dLoc=loc, dScale=scale)
    else:
        distribution = distributionToUse()

    intervals = np.linspace(0, 1, num=graphSections)
    intervalHeights = distribution(intervals)

    prefixSum = np.append([0], np.cumsum(intervalHeights))
    medianLoc = np.searchsorted(prefixSum, prefixSum[-1] / 2)

    for trial in tqdm(range(trials)):
        # Recreate distribution if necessary
        if recreateDistribution and trial % trialsPerRecreation == 0:
            distribution = distributionToUse()
            intervalHeights = distribution(intervals)

            prefixSum = np.append([0], np.cumsum(intervalHeights))
            medianLoc = np.searchsorted(prefixSum, prefixSum[-1] / 2)

        # Sorted list of candidates
        candidates = []

        if randomizeCandidates:
            # Randomly pick candidates from voter distribution
            while len(candidates) < numCandidates:
                randomCandidate = random.randint(0, math.floor(prefixSum[-1]) * 5000) / 5000.
                candidateLocation = np.searchsorted(prefixSum, randomCandidate)

                if candidateLocation != medianLoc:
                    candidates.append(candidateLocation)

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
            # Generate random left candidates
            while len(candidates) < leftCandidates:
                candidates.append(random.randrange(1, medianLoc))

            # Generate random right candidates
            while len(candidates) < rightCandidates:
                candidates.append(random.randrange(medianLoc + 1, graphSections))

            candidates.sort()

        # Find election winners
        CESWinner = findCESWinnerValue(prefixSum, medianLoc, candidates, leftCandidates, rightCandidates)
        RCVWinner = findRCVWinnerValue(prefixSum, candidates)

        CESPolarization.append(abs(CESWinner - medianLoc) * GRAPH_SCALE / graphSections)
        RCVPolarization.append(abs(RCVWinner - medianLoc) * GRAPH_SCALE / graphSections)

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


# runAndShowGeneralDistributionVoters(nLoc=0.5, nScale=0.2, nTrials=1000000)
