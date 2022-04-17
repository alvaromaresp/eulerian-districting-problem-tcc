class Instance():

    def __init__(self, fileName: str, num_depots):
        self.fileName = fileName
        self.num_depots = num_depots



def instanciate():

    return [
        Instance("..\Instances\lpr\Lpr-a-01.txt", 3),
        Instance("..\Instances\lpr\Lpr-a-02.txt", 3),
        Instance("..\Instances\lpr\Lpr-a-02.txt", 2),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 2),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 3),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 4),
        Instance("..\Instances\lpr\Lpr-a-03.txt", 5),
        Instance("..\Instances\lpr\Lpr-a-04.txt", 4),
        Instance("..\Instances\lpr\Lpr-a-05.txt", 4),
        Instance("..\Instances\lpr\Lpr-b-01.txt", 2),
        Instance("..\Instances\lpr\Lpr-b-01.txt", 3),
        Instance("..\Instances\lpr\Lpr-b-02.txt", 2),
        Instance("..\Instances\lpr\Lpr-b-03.txt", 4),
        Instance("..\Instances\lpr\Lpr-b-04.txt", 4),
        Instance("..\Instances\lpr\Lpr-b-05.txt", 6),
        Instance("..\Instances\lpr\Lpr-c-01.txt", 3),
        Instance("..\Instances\lpr\Lpr-c-02.txt", 3),
        Instance("..\Instances\lpr\Lpr-c-03.txt", 4),
        Instance("..\Instances\lpr\Lpr-c-04.txt", 3),
        Instance("..\Instances\lpr\Lpr-c-05.txt", 4)
    ]