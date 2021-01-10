from igraph import *
import numpy as np
import matplotlib.pyplot as plt
import warnings
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

    # Plot best-fit lines
    first_best_fit_x = xs[:147]
    first_best_fit_y = ys[:147]
    sec_best_fit_x = xs[147:]
    sec_best_fit_y = ys[147:]

    lambda1 = calc_best_fit(first_best_fit_x, first_best_fit_y)
    lambda2 = calc_best_fit(sec_best_fit_x, sec_best_fit_y)

    alpha1 = 15
    alpha2 = 4*10**5

    first_plot_lim_x = xs[30:147]
    sec_plot_lim_x = xs[147:-100]
    plot_best_fit(first_plot_lim_x, alpha1, lambda1)
    plot_best_fit(sec_plot_lim_x, alpha2, lambda2)

    plt.annotate(xy=[36, 0.0011], s="λ=" + str(lambda1))
    plt.annotate(xy=[145, 2*10**-5], s="λ=" + str(lambda2))

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

    # Plot best-fit lines
    best_fit_x = xs[100:]
    best_fit_y = ys[100:]

    lambda1 = calc_best_fit(best_fit_x, best_fit_y)

    alpha = 6

    plot_lim_x = xs[14:1170]
    plot_best_fit(plot_lim_x, alpha, lambda1)

    plt.annotate(xy=[36, 0.00018], s="λ=" + str(lambda1))

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

    # Plot best-fit lines
    first_best_fit_x = xs[:200]
    first_best_fit_y = ys[:200]
    sec_best_fit_x = xs[200:]
    sec_best_fit_y = ys[200:]

    lambda1 = calc_best_fit(first_best_fit_x, first_best_fit_y)
    lambda2 = calc_best_fit(sec_best_fit_x, sec_best_fit_y)

    alpha1 = 80
    alpha2 = 4.4

    first_plot_lim_x = xs[40:200]
    sec_plot_lim_x = xs[200:1800]
    plot_best_fit(first_plot_lim_x, alpha1, lambda1)
    plot_best_fit(sec_plot_lim_x, alpha2, lambda2)

    plt.annotate(xy=[25, 0.0015], s="λ=" + str(lambda1))
    plt.annotate(xy=[155, 2*10**-5], s="λ=" + str(lambda2))

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
    warnings.warn("long computation", Warning)
    print("Result:", graph.diameter())

    print("Calculating average path length...")
    warnings.warn("long computation", Warning)
    print("Result:", graph.average_path_length())
