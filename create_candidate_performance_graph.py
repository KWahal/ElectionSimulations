from general_distributions import runGeneralDistributionVoters
from candidate_graphs import computeStatistics
import matplotlib.pyplot as plt
import general_distributions as dist
from tqdm import tqdm
import numpy as np
from multiprocessing import Process, SimpleQueue
import time


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

        print(
            f"For {i} candidates, RCV is better or equal {betterOrEqual[i-3]} percent of the time"
        )
        print(f"Computed stats for {i}")

    plt.xlabel("Number of Candidates in Election")
    plt.ylabel("Share of Elections")

    # gray #333333

    color_one = "#E39FF6"
    color_two = "#9867C5"

    plt.fill_between(vals, betterOrEqual, color=color_one, alpha=0.4, label="No Worse")
    plt.fill_between(vals, tied, color=color_two, alpha=0.6, label="Tied")

    plt.scatter(vals, betterOrEqual, color=color_one)
    plt.scatter(vals, tied, color=color_two)

    # plt.scatter(vals, betterOrEqual, label="No Worse", color=color_one)
    # plt.scatter(vals, tied, label="Tied", color=color_two)
    plt.legend()
    plt.savefig("overall_graph.png")


NUM_MEANS = 5
NUM_DEVIATIONS = 5


def create_full_graph():
    plt.rcParams["figure.figsize"] = (12, 12)

    means = [0.5 + (0.1 * i) for i in range(NUM_MEANS)]
    deviations = [0.05 * (2**i) for i in range(NUM_DEVIATIONS)]

    figure, axis = plt.subplots(NUM_MEANS, NUM_DEVIATIONS)

    for i, mean in enumerate(means):
        for j, deviation in enumerate(deviations):
            tied = []
            betterOrEqual = []
            vals = []

            for NUM_CANDIDATES in range(3, 101):
                CES, RCV = runGeneralDistributionVoters(
                    loc=mean,
                    scale=deviation,
                    trials=10000,
                    numCandidates=NUM_CANDIDATES,
                )
                above, on, below, colors = computeStatistics(CES, RCV)

                total = len(CES)
                tied.append(float(on) / total)
                betterOrEqual.append((below + on) / float(total))
                vals.append(NUM_CANDIDATES)

                print(
                    f"For {NUM_CANDIDATES} candidates with mean {mean} and standard deviation {deviation}, RCV is better or equal {betterOrEqual[NUM_CANDIDATES-3]} percent of the time"
                )

            axis[i, j].set_title(f"μ = {mean}, σ = {deviation}")

            axis[i, j].tick_params(
                axis="both",
                which="both",
                bottom=True,
                left=True,
                right=False,
                top=False,
                labelbottom=True,
                labelleft=True,
            )

            color_one = "#E39FF6"
            color_two = "#9867C5"

            axis[i, j].fill_between(
                vals, betterOrEqual, color=color_one, alpha=0.4, label="No Worse"
            )
            axis[i, j].fill_between(
                vals, tied, color=color_two, alpha=0.6, label="Tied"
            )

            axis[i, j].scatter(vals, betterOrEqual, color=color_one)
            axis[i, j].scatter(vals, tied, color=color_two)

    figure.tight_layout()
    plt.savefig("all_graphs.png")
    plt.show()


def run_portion_of_trials(results, **kwargs):
    # Run one trial and save the results
    results.put(dist.runGeneralDistributionVoters(**kwargs))
    results.put(QUEUE_END)
    results.close()


GRAPH_SECTIONS = 50000
QUEUE_END = "END"


def run_sim_multiprocessed(numThreads=1, **kwargs):
    # Store list of results
    resultQueue = SimpleQueue()

    # Create processes and update number of trials
    processes = []
    kwargs["trials"] = kwargs["trials"] // numThreads

    for _ in range(numThreads):
        processes.append(
            Process(
                target=run_portion_of_trials,
                args=(resultQueue,),
                kwargs=kwargs,
            )
        )

    # Start each thread then wait for all to finish
    for t in processes:
        t.start()

    # Get all results and return them combined
    results = []
    doneCnt = 0
    while doneCnt < numThreads:
        res = resultQueue.get()

        if res == QUEUE_END:
            doneCnt += 1
        else:
            results.append(res)

    combResults = [[] for _ in range(len(results[0]))]
    for res in results:
        for i, vals in enumerate(res):
            combResults[i] += vals

    for res in combResults:
        assert len(res) == kwargs["trials"] * numThreads

    return tuple(combResults)


def create_overall_spline_graph(
    distsToCreate=5000, runsPerDist=5, tilt=0.5, numThreads=1
):
    totalNumTrials = distsToCreate * runsPerDist

    better = []
    betterOrEqual = []
    vals = []

    for i in tqdm(range(3, 101)):
        results = run_sim_multiprocessed(
            numThreads=numThreads,
            trials=totalNumTrials,
            numCandidates=i,
            isNormal=False,
            graphSections=GRAPH_SECTIONS,
            distributionToUse=dist.randomSplineDistribution,
            recreateDistribution=True,
            trialsPerRecreation=runsPerDist,
            tilt=tilt,
        )

        # Calculate number of times better and better or equal
        numBetter = 0
        numBetterOrEqual = 0
        for rcv, ces in zip(*results):
            if rcv <= ces:
                numBetterOrEqual += 1
            if rcv < ces:
                numBetter += 1

        # Update with information from this trial
        vals.append(i)

        better.append(numBetter / totalNumTrials)
        betterOrEqual.append(numBetterOrEqual / totalNumTrials)

        print(
            f"For {i} candidates, RCV is better or equal {betterOrEqual[-1]} percent of the time"
        )
        print(f"Computed stats for {i}")

    plt.xlabel("Number of Candidates in Election")
    plt.ylabel("Share of Elections")

    # Print results
    print(better)
    print(betterOrEqual)

    color_one = "#E39FF6"
    color_two = "#9867C5"

    plt.fill_between(vals, better, color=color_two, alpha=0.6, label="Better")
    plt.fill_between(vals, betterOrEqual, color=color_one, alpha=0.4, label="No Worse")

    plt.scatter(vals, better, color=color_two)
    plt.scatter(vals, betterOrEqual, color=color_one)

    plt.legend()
    plt.show()
    plt.savefig(f"Overall_spline_graph_{distsToCreate}_trials_tilt_{tilt}.png")
    plt.clf()


def create_tilt_graphs():
    for mult in range(3):
        tilt = 0.5 + 0.1 * mult
        create_overall_spline_graph(distsToCreate=10000, tilt=tilt, numThreads=32)


def create_lower_tilt_graphs():
    for mult in range(3):
        tilt = 0.8 + 0.1 * mult
        create_overall_spline_graph(distsToCreate=10000, tilt=tilt, numThreads=32)


def run_limited_votes_variations(distsToCreate=5000, runsPerDist=5, numThreads=32):
    results = []
    totalTrials = distsToCreate * runsPerDist

    for i in tqdm(range(3, 101)):
        data = run_sim_multiprocessed(
            numThreads=numThreads,
            trials=totalTrials,
            numCandidates=i,
            isNormal=False,
            graphSections=GRAPH_SECTIONS,
            distributionToUse=dist.randomSplineDistribution,
            recreateDistribution=True,
            trialsPerRecreation=runsPerDist,
            independentRegions=(0.5, 0.5),
            runLimitedVotes=True,
        )

        results.append(list(data))

    # Create numpy arr from results and print to csv
    arr = np.array(results)
    np.save("limited_voting_variations_output.npy", arr)

def run_all_voting_methods(distsToCreate=5000, runsPerDist=5, numThreads=32):
    results = []
    totalTrials = distsToCreate * runsPerDist

    for i in tqdm(range(3, 101)):
        data = run_sim_multiprocessed(
            numThreads=numThreads,
            trials=totalTrials,
            numCandidates=i,
            isNormal=False,
            graphSections=GRAPH_SECTIONS,
            distributionToUse=dist.randomSplineDistribution,
            recreateDistribution=True,
            trialsPerRecreation=runsPerDist,
            runOtherVotingMethods=True,
            runLimitedVotes=True,
        )

        results.append(list(data))

    # Create numpy arr from results and print to csv
    arr = np.array(results)
    np.save("all_voting_variations_output.npy", arr)

if __name__ == "__main__":
    run_all_voting_methods(distsToCreate=10000, runsPerDist=5, numThreads=32)
