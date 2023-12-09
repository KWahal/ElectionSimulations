import matplotlib.pyplot as plt
import general_distributions as dist
from scipy.stats import norm
import numpy as np

NUM_MEANS = 5
NUM_DEVIATIONS = 5
TRIALS = 500
NUM_TO_SHOW = 1000
NUM_CANDIDATES = 4

ABOVE_COLOR = 'red'
EQUAL_COLOR = 'yellow'
BELOW_COLOR = 'green'

DISPLAY_DISTRIBUTION_MODE = False
NUM_GRAPH_SECTIONS = 50000

def percentage(val, total):
    return round(100 * float(val)/total, 2)

def computeStatistics(CESPol, RCVPol):
    numAbove = 0
    numEqual = 0
    numBelow = 0
    colorArr = []

    for i, pol in enumerate(CESPol):
        if RCVPol[i] > pol:
            numAbove += 1
            colorArr.append(ABOVE_COLOR)
        elif RCVPol[i] == pol:
            numEqual += 1
            colorArr.append(EQUAL_COLOR)
        else:
            numBelow += 1
            colorArr.append(BELOW_COLOR)

    return numAbove, numEqual, numBelow, colorArr

def partition(CESPol, RCVPol, colorArr):
    above = [[], []]
    equal = [[], []]
    below = [[], []]

    for i in range(min(len(CESPol), NUM_TO_SHOW)):
        if colorArr[i] == ABOVE_COLOR:
            above[0].append(CESPol[i])
            above[1].append(RCVPol[i])
        elif colorArr[i] == EQUAL_COLOR:
            equal[0].append(CESPol[i])
            equal[1].append(RCVPol[i])
        elif colorArr[i] == BELOW_COLOR:
            below[0].append(CESPol[i])
            below[1].append(RCVPol[i])

    return above, equal, below

def showGraphArray():
    plt.rcParams["figure.figsize"] = (12, 12)

    means = [0.5 + (0.1 * i) for i in range(NUM_MEANS)]
    deviations = [0.05 * (2 ** i) for i in range(NUM_DEVIATIONS)]

    figure, axis = plt.subplots(NUM_MEANS, NUM_DEVIATIONS)

    for i, mean in enumerate(means):
        for j, deviation in enumerate(deviations):
            if DISPLAY_DISTRIBUTION_MODE:
                intervals = np.linspace(0, 1, num=NUM_GRAPH_SECTIONS)
                axis[i, j].plot(intervals, norm.pdf(intervals, loc=mean, scale=deviation))
                axis[i, j].set_ylim(0, 2)
                axis[i, j].set_xlim(0, 1)
                axis[i, j].tick_params(axis='y', which='both', bottom=False,
                                       left=False, right=False, top=False,
                                       labelbottom=False, labelleft=False)
                continue

            CESPol, RCVPol = \
                dist.runGeneralDistributionVoters(loc=mean, scale=deviation, trials=TRIALS, numCandidates=NUM_CANDIDATES)

            above, on, below, colors = computeStatistics(CESPol, RCVPol)

            aboveList, onList, belowList = partition(CESPol, RCVPol, colors)

            axis[i, j].set_title(f'μ = {mean}, σ = {deviation}')

            axis[i, j].tick_params(axis='both', which='both', bottom=False,
                                   left=False, right=False, top=False,
                                   labelbottom=False, labelleft=False)

            axis[i, j].scatter(aboveList[0], aboveList[1], color=ABOVE_COLOR, label=f"{percentage(above, TRIALS)}%")
            axis[i, j].scatter(onList[0], onList[1], color=EQUAL_COLOR, label=f"{percentage(on, TRIALS)}%")
            axis[i, j].scatter(belowList[0], belowList[1], color=BELOW_COLOR, label=f"{percentage(below, TRIALS)}%")

            totalMax = max(max(CESPol[:NUM_TO_SHOW]), max(RCVPol[:NUM_TO_SHOW]))
            axis[i, j].set_xlim(0, totalMax)
            axis[i, j].set_ylim(0, totalMax)
            axis[i, j].legend(loc="upper left")

            print(f"{mean}, {deviation}, {percentage(below, TRIALS)}, {percentage(on, TRIALS)}, {percentage(above, TRIALS)}")

    figure.tight_layout()
    plt.savefig('GraphArray.png')
    plt.show()


if __name__ == '__main__':
    showGraphArray()
