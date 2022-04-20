class Instance():

    def __init__(self, fileName: str, num_depots, num_nodes):
        self.fileName = fileName
        self.num_depots = num_depots
        self.num_nodes = num_nodes



def instanciate():

    return [
        Instance("..\Instances\lpr\Lpr-a-01.txt", 3, 28),
        Instance("..\Instances\lpr\Lpr-a-02.txt", 3, 53),
        Instance("..\Instances\lpr\Lpr-a-02.txt", 2, 53),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 2, 143),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 3, 143),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 4, 143),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 5, 143),
        Instance("..\Instances\lpr\Lpr-a-04.txt", 4, 195),
        Instance("..\Instances\lpr\Lpr-a-05.txt", 4, 321),
        Instance("..\Instances\lpr\Lpr-b-01.txt", 2, 28),
        Instance("..\Instances\lpr\Lpr-b-01.txt", 3, 28),
        Instance("..\Instances\lpr\Lpr-b-02.txt", 2, 53),
        Instance("..\Instances\lpr\Lpr-b-03.txt", 4, 163),
        Instance("..\Instances\lpr\Lpr-b-04.txt", 4, 248),
        Instance("..\Instances\lpr\Lpr-b-05.txt", 6, 401),
        Instance("..\Instances\lpr\Lpr-c-01.txt", 3, 28),
        Instance("..\Instances\lpr\Lpr-c-02.txt", 3, 43),
        Instance("..\Instances\lpr\Lpr-c-03.txt", 4, 163),
        Instance("..\Instances\lpr\Lpr-c-04.txt", 3, 277),
        Instance("..\Instances\lpr\Lpr-c-05.txt", 4, 369)
    ]