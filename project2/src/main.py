from social_network import *
from activity import *
from igraph import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    args = parser.parse_args()

    if args.dataset == "input/higgs-social_network.edgelist":
        # Read graph
        graph = Graph.Read(args.dataset, "edgelist")
        n_nodes = graph.vcount()
        n_edges = graph.ecount()
        
        # Calculate degree distributions
        calc_out_degree(graph)
        calc_in_degree(graph)
        calc_total_degree(graph)

        # Calculate graph assortativity degree
        calc_assort_degree(graph)
        
        # Calculate clustering properties
        calc_clustering(graph, n_nodes, n_edges)
        
        # Calculate shortest path measures
        calc_short_path(graph)

    elif args.dataset == "input/higgs-activity_time.txt":
        activity_list = parse_activity_time(args.dataset)
        
        activated_users = build_activated_users(activity_list)
        plot_activated_users(activated_users)

        plot_activity_psec(activity_list)
