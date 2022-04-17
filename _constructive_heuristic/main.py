import numpy
import time
from instances import instanciate, Instance
from model import ConstructiveModel
from data_processing import processFile
from graph import Graph

def main():
    file = None

    # if (len(sys.argv) > 1):
    #     file = open(sys.argv[1])
    # else:
    #     exit()

    # while True:
    #     graph = Graph()
    #     instance = Instance("..\Instances\lpr\Lpr-b-02.txt", 2)
    #     file = open(instance.fileName)
    #     processFile(file, graph, instance.num_depots)
    #     model = ConstructiveModel()
    #     model.execute(graph, tau_1=1)
    instances = instanciate()


    tau_1_values = [1, 0.75, 0.5, 0.25, 0.1]


    model = ConstructiveModel()

    for type in ["heuristic", "demand", "objective"]:
        result_file = open("result-" + type + "-" + str(time.time()) + ".txt", "a")

        result_file.write("|V| - |E| - |D| -  tau_1  - \% Lost Parity - Obj. Function - Depots distance mean - t(s)")
        result_file.write("\n")
        for i in instances:
            for t in tau_1_values:
                lost_parity = []
                obj_func = []
                depot_distance = []
                time_exec = []
                for j in range(10):
                    graph = Graph()
                    file = open(i.fileName)
                    processFile(file, graph, i.num_depots)
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