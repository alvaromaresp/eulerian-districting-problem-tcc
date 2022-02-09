from mip import Model, xsum, minimize, BINARY, INTEGER

import sys

from graph import Graph
from edge import Edge

from data_processing import *

import functools


file = None

if (len(sys.argv) > 1):
    file = open(sys.argv[1])
else:
    exit()

graph = Graph()

processFile(file, graph)

graph.addDepot(1)
graph.addDepot(2)
graph.addDepot(3)


d_ = functools.reduce(lambda acc, actual : acc + (actual.demand if actual.demand != None else 0), graph.edges, 0) / len(graph.depots)

tau_1 = 0.10
tau_2 = 0.10

m = Model(sense=MINIMIZE, solver_name=CBC)

# Variáveis de decisão
x_pe = [[m.add_var(var_type=BINARY) for _ in graph.edges] for _ in graph.depots]
w_pi = [[m.add_var(var_type=BINARY) for _ in graph.nodes] for _ in graph.depots]
z_ip_bin = [[m.add_var(var_type=BINARY) for _ in graph.nodes] for _ in graph.depots]
z_ip = [[m.add_var(var_type=INTEGER) for _ in graph.nodes] for _ in graph.depots]
r_i = [m.add_var(var_type=BINARY) for _ in graph.nodes]

# 1

m.objective = minimize(
    xsum(
        graph.getShortestPathEdgeLen(
            graph.getShortestPathEdgeLen(edge, depot) *
                x_pe[e][p] for e, edge in enumerate(graph.edges) for p, depot in enumerate(graph.depots)
        )
    )
)

# 2
for e in enumerate(graph.edges):
    m += xsum(x_pe[p][e] for p in enumerate(graph.depots)) == 1


# 4
for p in enumerate(graph.depots):
    m += xsum(e.demand * x_pe[p][e] for e in enumerate(graph.edges)) <= d_*(1 + tau_1) 

# 5
for p in enumerate(graph.depots):
    m += xsum(e.demand * x_pe[p][e] for e in enumerate(graph.edges)) >= d_*(1 - tau_1) 

# 6
for p in enumerate(graph.depots):
    for i, node in enumerate(graph.nodes):
        m += xsum(x_pe[p][e] for e in node.incident_edges) <= graph.bigM * w_pi[p][i]

# 7
for p in enumerate(graph.depots):
    for i in graph.nodes:
        m += xsum(x_pe[p][e] for e in i.incident_edges) >= w_pi[p][i]

# 8
for p in enumerate(graph.depots):
    for i, node in enumerate(graph.nodes):
        m += xsum(x_pe[p][e] for e in node.incident_edges) == 2 * z_ip[p][i] + z_ip[p][i]

# 9
for i in graph.even_degree_nodes:
    m += xsum(z_ip_bin[i.id - 1][p] for p in enumerate(graph.depots)) >= r_i[i.id - 1]

# 10
for i in graph.even_degree_nodes:
    m += xsum(z_ip_bin[i.id - 1][p] for p in enumerate(graph.depots)) <= r_i[i.id - 1] * len(graph.depots)

# 11
for i in graph.odd_degree_nodes:
    m += xsum(z_ip_bin[i.id - 1][p] for p in enumerate(graph.depots)) - 1 >= r_i[i.id - 1]

# 12
for i in graph.odd_degree_nodes:
    m += xsum(z_ip_bin[i.id - 1][p] for p in enumerate(graph.depots)) - 1 <= r_i[i.id - 1] * len(graph.depots)

# 13
m += xsum(r_i[i] for i in enumerate(graph.nodes)) * (1/len(graph.nodes)) <= tau_2
