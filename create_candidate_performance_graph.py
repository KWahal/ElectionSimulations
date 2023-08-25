from general_distributions import runGeneralDistributionVoters
from candidate_graphs import computeStatistics
import matplotlib.pyplot as plt


def create_one_graph():
    tied = []
    betterOrEqual = []
    vals = []

    for i in range(3, 6):
        CES, RCV = runGeneralDistributionVoters(numCandidates=i, trials=10000)
        above, on, below, colors = computeStatistics(CES, RCV)

        total = len(CES)
        tied.append(float(on) / total)
        betterOrEqual.append((below + on) / float(total))
        vals.append(i)

        print(f'For {i} candidates, RCV is better or equal {betterOrEqual[i-3]} percent of the time')
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
    plt.savefig('overall_graph.png')



NUM_MEANS = 5
NUM_DEVIATIONS = 5

def create_full_graph():
    plt.rcParams["figure.figsize"] = (12, 12)

    means = [0.5 + (0.1 * i) for i in range(NUM_MEANS)]
    deviations = [0.05 * (2 ** i) for i in range(NUM_DEVIATIONS)]

    figure, axis = plt.subplots(NUM_MEANS, NUM_DEVIATIONS)

    for i, mean in enumerate(means):
        for j, deviation in enumerate(deviations):

            tied = []
            betterOrEqual = []
            vals = []

            for NUM_CANDIDATES in range(3, 101):
                CES, RCV = runGeneralDistributionVoters(loc=mean, scale=deviation, trials=10000, numCandidates=NUM_CANDIDATES)
                above, on, below, colors = computeStatistics(CES, RCV)

                total = len(CES)
                tied.append(float(on) / total)
                betterOrEqual.append((below + on) / float(total))
                vals.append(NUM_CANDIDATES)

                print(f'For {NUM_CANDIDATES} candidates with mean {mean} and standard deviation {deviation}, RCV is better or equal {betterOrEqual[NUM_CANDIDATES-3]} percent of the time')

            axis[i, j].set_title(f'μ = {mean}, σ = {deviation}')

            axis[i, j].tick_params(axis='both', which='both', bottom=True,
                                   left=True, right=False, top=False,
                                   labelbottom=True, labelleft=True)
            
            color_one = "#E39FF6"
            color_two = "#9867C5"

            axis[i, j].fill_between(vals, betterOrEqual, color=color_one, alpha=0.4, label="No Worse")
            axis[i, j].fill_between(vals, tied, color=color_two, alpha=0.6, label="Tied")

            axis[i, j].scatter(vals, betterOrEqual, color=color_one)
            axis[i, j].scatter(vals, tied, color=color_two)

    figure.tight_layout()
    plt.savefig('all_graphs.png')
    plt.show()

create_full_graph()