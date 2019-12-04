from igraph import Graph, plot, Layout, RainbowPalette
from math import sin, cos
import collections

filename = "higgs-social_network.edgelist"

# Read graph
graph = Graph.Read(filename, "edgelist")
coreness = graph.coreness()
vertexes = {}

for i in range(0, len(coreness)):
    vertexes[i] = coreness[i]

# sort
vertexes = sorted(vertexes, key=vertexes.get, reverse=False)

# Set vertexes color
pal = RainbowPalette(n=max(coreness)+1)  # n=max(coreness))

for v in graph.vs:
    v["color"] = pal.get(coreness[v.index])
    if graph.degree(v.index) <= 19:
        v["size"] = 32
    elif graph.degree(v.index) <= 76:
        v["size"] = 24
    elif graph.degree(v.index) <= 304:
        v["size"] = 20
    elif graph.degree(v.index) <= 1216:
        v["size"] = 15
    elif graph.degree(v.index) <= 4864:
        v["size"] = 12
    elif graph.degree(v.index) <= 19456:
        v["size"] = 10
    else:
        v["size"] = 6


shells = list(set(coreness))
shells.sort()

layout = Layout(dim=2)

frequency = {}
for item in coreness:
    if item not in frequency:
        frequency[item] = 0
    frequency[item] += 1

for shell in shells:
    print(f"Calculating {shell} from {len(shells)-1}")
    v = (1 - ((shell) / max(shells)))
    nodes_in_shell = frequency[shell]
    angles = []
    angle = 0
    while angle <= 360.1:
        angles.append(angle)
        angle += 360 / nodes_in_shell

    angles = angles[:-1]
    for angle in angles:
        layout.append([sin(angle) * v, cos(angle) * v])

plot(graph, target="coreness.png", bbox=(0, 0, 2000, 2000), layout=layout,
     palette=pal, edge_width=0, edge_arrow_size=0, edge_arrow_width=10**-10, vertex_frame_width=0,
     vertex_order=vertexes)
