import matplotlib.pyplot as plt
import general_distributions as dist
import candidate_graphs as cand_graphs

import numpy as np

TRIALS = 25000000
TRIALS_PER_RECREATION = 5000
NUM_CANDIDATES = 9

NUM_GRAPH_SECTIONS = 50000

DISPLAY_EXAMPLE_GRAPH = False

if DISPLAY_EXAMPLE_GRAPH:
    displayDist = dist.randomSplineDistribution()
    intervals = np.linspace(0, 1, num=NUM_GRAPH_SECTIONS)
    plt.plot(intervals, displayDist(intervals))
    plt.xlim(0, 1)
    plt.show()

CESPol, RCVPol = dist.runGeneralDistributionVoters(trials=TRIALS, numCandidates=NUM_CANDIDATES, isNormal=False,
                                                   distributionToUse=dist.randomSplineDistribution, recreateDistribution=True,
                                                   trialsPerRecreation=TRIALS_PER_RECREATION)

above, on, below, colors = cand_graphs.computeStatistics(CESPol, RCVPol)
print(f'Above: {cand_graphs.percentage(above, TRIALS)}, On: {cand_graphs.percentage(on, TRIALS)}, Below: {cand_graphs.percentage(below, TRIALS)}')

cand_graphs.percentage(above, TRIALS)
