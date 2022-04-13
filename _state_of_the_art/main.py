import sys
from model import SOTA_Model

from data_processing import processFile
from graph import Graph

def main():
    file = None

    if (len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        exit()

    graph = Graph()

    processFile(file, graph)
    
    print(graph.G.nodes())
    model = SOTA_Model()

    model.execute(graph)

if __name__ == "__main__":
    main()