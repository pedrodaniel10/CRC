from activity import *
from igraph import *
import argparse
import social_network as socl
import reply_network as rply
import retweet_network as rtt
import mention_network as ment

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    args = parser.parse_args()

    if args.dataset.endswith("higgs-social_network.edgelist"):
        # Read graph
        graph = Graph.Read(args.dataset, "edgelist")
        n_nodes = graph.vcount()
        n_edges = graph.ecount()
        print(f"Nodes: {n_nodes}")
        print(f"Edges: {n_edges}")

        # Calculate degree distributions
        socl.calc_out_degree(graph)
        socl.calc_in_degree(graph)
        socl.calc_total_degree(graph)

        # Calculate graph assortativity degree
        socl.calc_assort_degree(graph)

        # Calculate clustering properties
        socl.calc_clustering(graph, n_nodes, n_edges)

        # Calculate shortest path measures
        socl.calc_short_path(graph)
    elif args.dataset.endswith("higgs-reply_network.edgelist"):
        # Read graph
        graph = Graph.Read(args.dataset, "edgelist")
        n_nodes = graph.vcount()
        n_edges = graph.ecount()
        print(f"Nodes: {n_nodes}")
        print(f"Edges: {n_edges}")

        # Calculate degree distributions
        rply.calc_out_degree(graph)
        rply.calc_in_degree(graph)
        rply.calc_total_degree(graph)

        # Calculate graph assortativity degree
        rply.calc_assort_degree(graph)

        # Calculate clustering properties
        rply.calc_clustering(graph, n_nodes, n_edges)

        # Calculate shortest path measures
        rply.calc_short_path(graph)
    elif args.dataset.endswith("higgs-retweet_network.edgelist"):
        # Read graph
        graph = Graph.Read(args.dataset, "edgelist")
        n_nodes = graph.vcount()
        n_edges = graph.ecount()
        print(f"Nodes: {n_nodes}")
        print(f"Edges: {n_edges}")

        # Calculate degree distributions
        rtt.calc_out_degree(graph)
        rtt.calc_in_degree(graph)
        rtt.calc_total_degree(graph)

        # Calculate graph assortativity degree
        rtt.calc_assort_degree(graph)

        # Calculate clustering properties
        rtt.calc_clustering(graph, n_nodes, n_edges)

        # Calculate shortest path measures
        rtt.calc_short_path(graph)
    elif args.dataset.endswith("higgs-mention_network.edgelist"):
        # Read graph
        graph = Graph.Read(args.dataset, "edgelist")
        n_nodes = graph.vcount()
        n_edges = graph.ecount()
        print(f"Nodes: {n_nodes}")
        print(f"Edges: {n_edges}")

        # Calculate degree distributions
        ment.calc_out_degree(graph)
        ment.calc_in_degree(graph)
        ment.calc_total_degree(graph)

        # Calculate graph assortativity degree
        ment.calc_assort_degree(graph)

        # Calculate clustering properties
        ment.calc_clustering(graph, n_nodes, n_edges)

        # Calculate shortest path measures
        ment.calc_short_path(graph)

    elif args.dataset.endswith("higgs-activity_time.txt"):
        activity_list = parse_activity_time(args.dataset)

        activated_users = build_activated_users(activity_list)
        plot_activated_users(activated_users)

        plot_activity_psec(activity_list)

        plot_activity_density(activity_list)
