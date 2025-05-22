import os


def readFromFile(filename):
    if not os.path.exists(filename):
        raise Exception("File does not exists")
    file = open(filename, "r")
    line = file.readline()
    return line
