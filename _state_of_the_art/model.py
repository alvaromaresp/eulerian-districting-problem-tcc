from mip import Model, xsum, minimize, BINARY, INTEGER, CBC

from graph import Graph
import functools

class SOTA_Model():

    def execute(self, graph : Graph):
        d_ = functools.reduce(lambda acc, actual : acc + (actual.demand if actual.demand != None else 0), graph.edges, 0) / len(graph.depots)

        tau_1 = 0.80
        tau_2 = 0.80

        m = Model(sense=minimize, solver_name=CBC)

        # Variáveis de decisão
        x_pe = [[m.add_var(name = "X_" + str(p) + "_" + str(e), var_type=BINARY) for e, _ in enumerate(graph.edges)] for p, _ in enumerate(graph.depots)]
        w_pi = [[m.add_var(name = "W_" + str(p) + "_" + str(i), var_type=BINARY) for i, _ in enumerate(graph.nodes)] for p, _ in enumerate(graph.depots)]
        z_ip_bin = [[m.add_var(name = "Zbin_" + str(p) + "_" + str(i), var_type=BINARY) for i, _ in enumerate(graph.nodes)] for p, _ in enumerate(graph.depots)]
        z_ip = [[m.add_var(name = "Z_" + str(p) + "_" + str(i), var_type=INTEGER) for i, _ in enumerate(graph.nodes)] for p, _ in enumerate(graph.depots)]
        r_i = [m.add_var(name = "r_" + str(i), var_type=BINARY) for i, _ in enumerate(graph.nodes)]

        # 1

        # for i in graph.nodes:
        #     print(' ------ NODE ------ ' + str(i.id))
        #     i.printEdges()

        m.objective = minimize(
            xsum(
                graph.getShortestPathEdgeLen(edge, depot) * x_pe[p][e]
                for e, edge in enumerate(graph.edges) for p, depot in enumerate(graph.depots)
            )
        )

        # 2
        for e, _ in enumerate(graph.edges):
            m += xsum(x_pe[p][e] for p, _ in enumerate(graph.depots)) == 1, "CONSTRAINT_2"


        # 4
        for p, _ in enumerate(graph.depots):
            m += xsum(edge.demand * x_pe[p][e] for e, edge in enumerate(graph.edges)) <= d_*(1 + tau_1), "CONSTRAINT_4"

        # 5
        for p, _ in enumerate(graph.depots):
            m += xsum(edge.demand * x_pe[p][e] for e, edge in enumerate(graph.edges)) >= d_*(1 - tau_1), "CONSTRAINT_5"

        # 6
        for p, _ in enumerate(graph.depots):
            for i in graph.nodes:
                m += xsum(x_pe[p][e.id] for _ , e in enumerate(i.edges)) <= graph.bigM * w_pi[p][i.id], "CONSTRAINT_6"

        # 7
        for p, _ in enumerate(graph.depots):
            for i in graph.nodes:
                m += xsum(x_pe[p][e.id] for _ , e in enumerate(i.edges)) >= w_pi[p][i.id], "CONSTRAINT_7"

        # 8
        for p, _ in enumerate(graph.depots):
            for i in graph.nodes:
                m += xsum(x_pe[p][e.id] for _ , e in enumerate(i.edges)) == 2 * z_ip[p][i.id] + z_ip[p][i.id], "CONSTRAINT_8"

        # 9
        for i in graph.even_degree_nodes:
            m += xsum(z_ip_bin[p][i.id] for p, _ in enumerate(graph.depots)) >= r_i[i.id], "CONSTRAINT_9"

        # 10
        for i in graph.even_degree_nodes:
            m += xsum(z_ip_bin[p][i.id] for p, _ in enumerate(graph.depots)) <= r_i[i.id] * len(graph.depots), "CONSTRAINT_10"

        # 11
        for i in graph.odd_degree_nodes:
            m += xsum(z_ip_bin[p][i.id] for p, _ in enumerate(graph.depots)) - 1 >= r_i[i.id], "CONSTRAINT_11"

        # 12
        for i in graph.odd_degree_nodes:
            m += xsum(z_ip_bin[p][i.id] for p, _ in enumerate(graph.depots)) - 1 <= r_i[i.id] * len(graph.depots), "CONSTRAINT_12"

        # 13
        m += xsum(r_i[i.id] for i in graph.nodes) * (1/len(graph.nodes)) <= tau_2, "CONSTRAINT_13"

        m.write('model.lp')

        m.optimize()


        graph.printGraph(x_pe)