from general_distributions import runGeneralDistributionVoters
from candidate_graphs import computeStatistics
import matplotlib.pyplot as plt

tied = []
betterOrEqual = []
vals = []

for i in range(3, 10):
    CES, RCV = runGeneralDistributionVoters(numCandidates=i, trials=10000)
    above, on, below, colors = computeStatistics(CES, RCV)

    total = len(CES)
    tied.append(float(on) / total)
    betterOrEqual.append((below + on) / float(total))
    vals.append(i)

    print(f'Computed stats for {i}')

plt.xlabel("Number of Candidates in Election")
plt.ylabel("Share of Elections")

#gray #333333

color_one = "#E39FF6"
color_two = "#9867C5"

plt.fill_between(vals, betterOrEqual, color=color_one, alpha=0.4, label="No Worse")
plt.fill_between(vals, tied, color=color_two, alpha=0.6, label="Tied")

plt.scatter(vals, betterOrEqual, color=color_one)
plt.scatter(vals, tied, color=color_two)

# plt.scatter(vals, betterOrEqual, label="No Worse", color=color_one)
# plt.scatter(vals, tied, label="Tied", color=color_two)
plt.legend()
plt.show()
