
import glob
import shutil

data = glob.glob("./formatted/view/*")
data.sort()

# print(data)

def getFname(path):
    return path.split('/')[-1]

for index in range(0, len(data),2):
    fname = getFname(data[index])
    shutil.copyfile(data[index], f"./formatted/normal/{fname}")
    shutil.copyfile(data[index+1], f"./formatted/minimal/{fname}")
