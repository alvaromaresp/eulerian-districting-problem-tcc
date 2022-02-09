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
    for i in graph.nodes:
        m += xsum(x_pe[p][e] for e in i.incident_edges) <= graph.bigM * w_pi[p][i]

#7
for p in enumerate(graph.depots):
    for i in graph.nodes:
        m += xsum(x_pe[p][e] for e in i.incident_edges) >= w_pi[p][i]




# m.objective = minimize(xsum(p[i] * x[i] for i in I))

# # m += xsum(w[i] * x[i] for i in I) <= c

# m.optimize()

# selected = [i for i in I if x[i].x >= 0.99]
# print("selected items: {}".format(selected))

# x = [[model.add_var(var_type=BINARY) for e in E] for p in P]     1

# for e in E:
#     model += xsum(x[p][e] for p in P) == 1    2

# for p in P:
#     model += xsum(d[e]*x[p][e] for e in E) <= D*(1+tau)      4

# d[e] demanda do arco 

# definir paridade dos vértices no pré-processamento
# bpe menor caminho entre o menor caminho dos vértices


# model.objective = minimize(xsum(b[p][e]*x[p][e] for p in P for e in E))