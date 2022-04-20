import random
import numpy
import time
from instances import instanciate, Instance
from model import ConstructiveModel
from data_processing import processFile
from graph import Graph

def main():
    # file = None

    # while True:

    #     graph = Graph()
    #     instance = Instance("..\Instances\lpr\Lpr-b-02.txt", 2, 53)
    #     depots = []
    #     nodes_ids = [i + 1 for i in range(instance.num_nodes)]
    #     for _ in range(instance.num_depots):
            # random.shuffle(nodes_ids)
            # node = nodes_ids.pop()

            # depots.append(node)
    #     file = open(instance.fileName)
    #     processFile(file, graph, depots)
    #     model = ConstructiveModel()
    #     model.execute(graph, tau_1=1)
    instances = instanciate()


    tau_1_values = [1, 0.75, 0.5, 0.25, 0.1]

    timestamp =  str(time.time())
    result_demand_file = open("results/result-demand-" + timestamp + ".txt", "a")
    result_heuristic_file = open("results/result-heuristic-" + timestamp + ".txt", "a")
    result_objective_file = open("results/result-objective-" + timestamp + ".txt", "a")

    result_demand_file.write("FileName - |V| - |E| - |D| -  tau_1  - \% Lost Parity - Obj. Function - Depots distance mean - t(s)")
    result_heuristic_file.write("FileName - |V| - |E| - |D| -  tau_1  - \% Lost Parity - Obj. Function - Depots distance mean - t(s)")
    result_objective_file.write("FileName - |V| - |E| - |D| -  tau_1  - \% Lost Parity - Obj. Function - Depots distance mean - t(s)")

    model = ConstructiveModel()
    for i in instances:
        depots = []
        nodes_ids = [i + 1 for i in range(i.num_nodes)]
        for _ in range(i.num_depots):
            random.shuffle(nodes_ids)
            node = nodes_ids.pop()

            depots.append(node)
        for type in ["heuristic", "demand", "objective"]:
            result_file = None
            if (type == "heuristic"):
                result_file = result_heuristic_file
            elif (type == "demand"):
                result_file = result_demand_file
            elif (type == "objective"):
                result_file = result_objective_file

            for t in tau_1_values:
                lost_parity = []
                obj_func = []
                depot_distance = []
                time_exec = []
                for j in range(10):
                    graph = Graph()
                    file = open(i.fileName)
                    processFile(file, graph, depots)
                    result = model.execute(graph, tau_1=t, chosen_execution=type)
                    lost_parity.append(result[0])
                    obj_func.append(result[1])
                    depot_distance.append(result[2])
                    time_exec.append(result[3])


                result_file.write(i.fileName + " - ")
                result_file.write(str(len(graph.nodes)))
                result_file.write(" - ")
                result_file.write(str(len(graph.edges)))
                result_file.write(" - ")
                result_file.write(str(len(graph.depots)))
                result_file.write(" - ")
                result_file.write(str(t))
                result_file.write(" - ")
                result_file.write(str(numpy.mean(lost_parity)))
                result_file.write(" / ")
                result_file.write(str(numpy.std(lost_parity)))
                result_file.write(" - ")
                result_file.write(str(numpy.mean(obj_func)))
                result_file.write(" / ")
                result_file.write(str(numpy.std(obj_func)))
                result_file.write(" - ")
                result_file.write(str(numpy.mean(depot_distance)))
                result_file.write(" / ")
                result_file.write(str(numpy.std(depot_distance)))
                result_file.write(" - ")
                result_file.write(str(numpy.mean(time_exec)))
                result_file.write(" / ")
                result_file.write(str(numpy.std(time_exec)))
                result_file.write("\n")

        result_file.close()

if __name__ == "__main__":
    main()