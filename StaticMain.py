import os





def getLatestFile(dir):
    return sorted(os.listdir(dir)).pop()