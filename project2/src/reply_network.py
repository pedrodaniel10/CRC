from igraph import *
import argparse
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

BINS = 1


# Prints degree distribution properties
def print_degree_dist_props(histogram):
    print("Results:")
    print("Mean:", round(histogram.mean, 2))
    print("Variance:", round(histogram.var, 2))


# Calculates best fit power-law lambda
def calc_best_fit(xs, ys):
    data = []
    for i in range(len(xs)):
        for j in range(int(xs[i])):
            data.append(ys[i])
    result = power_law_fit(data)
    return round(result.alpha, 1)


# Plots best fit power laws for probability distribution
def plot_best_fit(x, alpha, lambda_val):
    plt.plot(x, alpha*x**-lambda_val, "-")


# Plots degree distribution from igraph.Histogram
def plot_degree_dist(histogram):
    # Get frequencies
    xs, ys = zip(*[(left, count) for left, _, count in histogram.bins()])
    xs = np.array(xs)
    ys = np.array(ys)

    del_indexes = np.array(xs[(ys < 1)], dtype="int")
    xs = np.delete(xs, del_indexes)
    ys = np.delete(ys, del_indexes)

    # Normalize
    ys_norm = [float(i)/sum(ys) for i in ys]

    # Plot out-degree distribution
    plt.plot(xs, ys_norm, marker=".", linestyle="", markersize=2)

    return xs, ys


# Calculates out-degree distribution
def calc_out_degree(graph):
    print("Calculating out-degree distribution...")
    plt.figure()

    histogram = graph.degree_distribution(BINS, mode=OUT)
    xs, ys = plot_degree_dist(histogram)

    lambda1 = calc_best_fit(xs, ys)

    alpha1 = 2*10**-3

    plot_best_fit(xs, alpha1, lambda1)

    plt.annotate(xy=[15, 0.0001], s="λ=" + str(lambda1))

    # Scales and labels
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Out-degree")
    plt.ylabel("Probability")
    plt.show()

    print_degree_dist_props(histogram)


# Calculates in-degree distribution
def calc_in_degree(graph):
    print("Calculating in-degree distribution...")
    plt.figure()

    histogram = graph.degree_distribution(BINS, mode=IN)
    xs, ys = plot_degree_dist(histogram)

    lambda1 = calc_best_fit(xs, ys)

    alpha = 10**-2

    plot_best_fit(xs[:55], alpha, lambda1)

    plt.annotate(xy=[25, 0.00018], s="λ=" + str(lambda1))

    # Scales and labels
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("In-degree")
    plt.ylabel("Probability")
    plt.show()

    print_degree_dist_props(histogram)


# Calculates total degree distribution
def calc_total_degree(graph):
    print("Calculating total degree distribution...")
    plt.figure()

    histogram = graph.degree_distribution(BINS, mode=ALL)
    xs, ys = plot_degree_dist(histogram)

    lambda1 = calc_best_fit(xs, ys)

    alpha1 = 10**-2

    plot_best_fit(xs[:55], alpha1, lambda1)

    plt.annotate(xy=[25, 0.0005], s="λ=" + str(lambda1))

    # Scales and labels
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Total degree")
    plt.ylabel("Probability")
    plt.show()

    print_degree_dist_props(histogram)


# Calculates graph assortativity degree
def calc_assort_degree(graph):
    print("Calculating assortativity degree...")
    result = graph.assortativity_degree()
    print("Result:", result)


def calc_clustering(graph, n_nodes, n_edges):
    print("Calculating the global clustering coefficient...")
    print("Result:", graph.transitivity_undirected())

    print("Calculating the average clustering coefficient (average of local coefficients)...")
    print("Result:", np.mean(graph.transitivity_local_undirected(mode="zero")))

    print("Calculating SCC...")
    scc = graph.components(mode="STRONG")
    largest_scc = scc.giant()

    largest_scc_nodes = largest_scc.vcount()
    largest_scc_edges = largest_scc.ecount()
    print("Nodes in largest SCC", largest_scc_nodes,
          "(" + str(round(largest_scc_nodes/n_nodes, 3)) + ")")
    print("Edges in largest SCC", largest_scc_edges,
          "(" + str(round(largest_scc_edges/n_edges, 3)) + ")")

    print("Calculating WCC...")
    wcc = graph.components(mode="WEAK")
    largest_wcc = wcc.giant()

    largest_wcc_nodes = largest_wcc.vcount()
    largest_wcc_edges = largest_wcc.ecount()
    print("Nodes in largest WCC", largest_wcc_nodes,
          "(" + str(round(largest_wcc_nodes/n_nodes, 3)) + ")")
    print("Edges in largest WCC", largest_wcc_edges,
          "(" + str(round(largest_wcc_edges/n_edges, 3)) + ")")


def calc_short_path(graph):
    print("Calculating diameter...")
    print("Result:", graph.diameter())

    print("Calculating average path length...")
    print("Result:", graph.average_path_length())
