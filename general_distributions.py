from scipy.interpolate import UnivariateSpline
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

LEFT_CANDIDATES = 1
RIGHT_CANDIDATES = 2

TRIALS = 1000
TRIALS_PER_DISTRIBUTION = 10
NUM_GRAPH_SECTIONS = 10000
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
    leftWin = findSimpleElectionWinnerValue(prefixSum[:medianLoc], candidates[:LEFT_CANDIDATES])
    rightWin = medianLoc + findSimpleElectionWinnerValue(prefixSum[medianLoc + 1:],
                                                         [candidate - medianLoc for candidate in candidates[LEFT_CANDIDATES: len(candidates)]])

    proportions = getVoterProportions(prefixSum, [leftWin, rightWin])
    return leftWin if proportions[0] >= proportions[1] else rightWin


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


def normalDistribution():
    return lambda distribution: norm.pdf(distribution, loc=0.5, scale=0.2)


def runGeneralDistributionVoters():
    CESPolarization = []
    RCVPolarization = []

    distribution = normalDistribution()
    for trial in range(int(TRIALS / TRIALS_PER_DISTRIBUTION)):
        # distribution = randomSplineDistribution()
        for trialDist in range(TRIALS_PER_DISTRIBUTION):
            intervals = np.linspace(0, 1, num=NUM_GRAPH_SECTIONS)
            intervalHeights = distribution(intervals)

            prefixSum = np.append([0], np.cumsum(intervalHeights))
            medianLoc = np.searchsorted(prefixSum, prefixSum[-1] / 2)

            # Ordered from left, moderate right, extreme right (index of candidates)
            candidates = []
            candidates.extend(sorted(np.random.choice(range(1, medianLoc), LEFT_CANDIDATES, replace=False)))
            candidates.extend(sorted(np.random.choice(range(medianLoc + 1, NUM_GRAPH_SECTIONS), RIGHT_CANDIDATES, replace=False)))

            CESWinner = findCESWinnerValue(prefixSum, medianLoc, candidates)
            RCVWinner = findRCVWinnerValue(prefixSum, candidates)

            CESPolarization.append(abs(CESWinner - medianLoc) * GRAPH_SCALE / NUM_GRAPH_SECTIONS)
            RCVPolarization.append(abs(RCVWinner - medianLoc) * GRAPH_SCALE / NUM_GRAPH_SECTIONS)

    # x-axis label
    plt.xlabel('Normal Election Polarization')
    # frequency label
    plt.ylabel('Ranked Choice Voting Polarization')
    # plot title
    plt.title('Generated RCV vs. CES Polarization')

    plt.scatter(CESPolarization, RCVPolarization, color='purple')
    plt.show()


runGeneralDistributionVoters()
