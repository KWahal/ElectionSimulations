# ElectionSimulations

This repo contains files to compute and visualize winners and extremism levels of a ranked-choice voting system and of the current election system (first-past-the-post, primary system).

```general_distributions.py``` provides code to uses a generic distribution voters to calculate the winners and extremism levels for both ranked-choice voting and the current election system.

```uniform_distributions.py``` uses a uniform distribution of voters, ```spline_graphs.py``` uses randomly generated cubic splines to generate a distribution, and ```candidate_graphs.py``` and ```create_candidate_performance_graph.py``` generate graphs to understand the results.

```standard_election.py``` uses a given number of randomly generated voters.

These files are used to inform the paper [Ranked Choice Voting, the Primaries System, and Political Extremism: Theory and Simulations](https://drive.google.com/file/d/1ZYXQWo0LX-ujtZSTNTUaJO9De9gbTnZU/view), co-authored by Karsen Wahal, Avidit Acharya, Rohan Cherivarala, and Robin Truax.
