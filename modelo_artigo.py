from mip import Model, xsum, minimize, BINARY, INTEGER

import networkx as nx
import matplotlib.pyplot  as plt

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

G = nx.Graph()

for e in graph.edges:
    G.add_edge(e.org, e.dst)

pos = nx.spring_layout(G, seed=225) 
nx.draw(G, pos, with_labels = True)
plt.show()

d_ = functools.reduce(lambda acc, actual : acc.demand + actual.demand, graph.edges) / len(graph.depots)
tau_1 = 0.10
tau_2 = 0.10

m = Model(sense=MINIMIZE, solver_name=CBC)

# 1
x = [[m.add_var(var_type=BINARY) for e in graph.edges] for p in graph.depots]


# 2
for (e, _) in enumerate(graph.edges):
    m += xsum(x[p][e] for (p, _) in enumerate(graph.depots)) == 1


# 4
for (p, _) in graph.depots:
    m += xsum(e.demand * x[p][e] for (e, _) in graph.edges) <= d_*(1 + tau_1) 

# 5
for (p, _) in graph.depots:
    m += xsum(e.demand * x[p][e] for (e, _) in graph.edges) >= d_*(1 - tau_1) 


#6



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