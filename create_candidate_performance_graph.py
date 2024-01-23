from general_distributions import runGeneralDistributionVoters
from candidate_graphs import computeStatistics
from spline_graphs import run_spline_dist
import matplotlib.pyplot as plt
import general_distributions as dist
from tqdm import tqdm
import threading
import numpy as np

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

def run_portion_of_trials(trials, numCandidates, graphSections, trialsPerRecreation,
                          tilt, better_or_equal_list, better_candidate_list, independentRegions=(0.5, 0.5)):
    # Run a portion of the trials
    ces, rcv = dist.runGeneralDistributionVoters(trials=trials, numCandidates=numCandidates, isNormal=False, graphSections=graphSections,
                                                 distributionToUse=dist.randomSplineDistribution, recreateDistribution=True,
                                                 trialsPerRecreation=trialsPerRecreation, tilt=tilt, independentRegions=independentRegions)
    
    # Calculate how many are better or equal and how many are tied
    better_or_equal_candidate_specific = 0
    better_candidate_specific = 0

    for j in range(len(ces)):
        if rcv[j] <= ces[j]:
            better_or_equal_candidate_specific += 1
        if rcv[j] < ces[j]:
            better_candidate_specific += 1
    
    # Add the value to the list so they can be accessed once all trials have been run
    better_or_equal_list.append(better_or_equal_candidate_specific)
    better_candidate_list.append(better_candidate_specific)

GRAPH_SECTIONS = 50000
def create_overall_spline_graph(distsToCreate=5000, runsPerDist=5, tilt=0.5, numThreads=1):
    totalNumTrials = distsToCreate * runsPerDist

    better = []
    betterOrEqual = []
    vals = []

    for i in tqdm(range(3, 101)):
        # Create lists for how many trials resulted in better or tied outcomes
        better_or_equal_list = []
        better_candidate_list = []

        # Create threads
        threads = []
        trialsPerThread = totalNumTrials // numThreads
        totalNumTrials = trialsPerThread * numThreads

        for _ in range(numThreads):
            threads.append(threading.Thread(target=run_portion_of_trials, args=(trialsPerThread, i, GRAPH_SECTIONS, runsPerDist, tilt,
                                                                                better_or_equal_list, better_candidate_list)))
        
        # Start each thread then wait for all to finish
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

        # Reconstruct better or equal and tied info
        better_or_equal_candidate_specific = sum(better_or_equal_list)
        better_candidate_specific = sum(better_candidate_list)

        # Update with information from this trial
        vals.append(i)

        betterOrEqual.append(better_or_equal_candidate_specific/totalNumTrials)
        better.append(better_candidate_specific/totalNumTrials)

        print(f'For {i} candidates, RCV is better or equal {betterOrEqual[-1]} percent of the time')
        print(f'Computed stats for {i}')

    plt.xlabel("Number of Candidates in Election")
    plt.ylabel("Share of Elections")

    #gray #333333

    # Print results
    print(betterOrEqual)
    print(better)

    color_one = "#E39FF6"
    color_two = "#9867C5"

    plt.fill_between(vals, betterOrEqual, color=color_one, alpha=0.4, label="No Worse")
    plt.fill_between(vals, better, color=color_two, alpha=0.6, label="Better")

    plt.scatter(vals, betterOrEqual, color=color_one)
    plt.scatter(vals, better, color=color_two)

    plt.legend()
    plt.show()
    plt.savefig(f'Overall_spline_graph_{distsToCreate}_trials_tilt_{tilt}.png')
    plt.clf()

def create_tilt_graphs():
    for mult in range(3):
        tilt = 0.5 + 0.1 * mult
        create_overall_spline_graph(distsToCreate=10000, tilt=tilt, numThreads=32)
    
def create_lower_tilt_graphs():
    for mult in range(3):
        tilt = 0.8 + 0.1 * mult
        create_overall_spline_graph(distsToCreate=10000, tilt=tilt, numThreads=32)

def run_all_voting_methods(distsToCreate=5000, runsPerDist=5):
    results = []
    totalTrials = distsToCreate * runsPerDist
    
    for i in tqdm(range(3, 101)):
        data = dist.runGeneralDistributionVoters(trials=totalTrials, numCandidates=i, isNormal=False, graphSections=GRAPH_SECTIONS,
                                                 distributionToUse=dist.randomSplineDistribution, recreateDistribution=True,
                                                 trialsPerRecreation=runsPerDist, runOtherVotingMethods=True)
        
        results.append(list(data))
    
    # Create numpt arr from results and print to csv
    arr = np.array(results)
    np.save('voting_variations_output.npy', arr)

def run_closed_variations(distsToCreate=5000, runsPerDist=5):
    totalTrials = distsToCreate * runsPerDist

    results = []

    for i in tqdm(range(3, 101)):
        data = dist.runGeneralDistributionVoters(trials=totalTrials, numCandidates=i, isNormal=False, graphSections=GRAPH_SECTIONS,
                                                distributionToUse=dist.randomSplineDistribution, recreateDistribution=True,
                                                trialsPerRecreation=runsPerDist, runClosed=True, independentRegions=(0.5, 0.5))
        
        results.append(list(data))

    # Create numpt arr from results and print to csv
    arr = np.array(results)
    np.save(f'voting_output_vary_indep.npy', arr)
    
# create_overall_spline_graph(distsToCreate=10000)
# create_tilt_graphs()
if __name__ == "__main__":
    run_closed_variations(10000)