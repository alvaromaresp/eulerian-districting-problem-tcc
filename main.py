import sys

def main():
    file = None

    if (len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        exit()

    graph = Graph()

    processFile(file, graph)

if __name__ == "__main__":
    main()