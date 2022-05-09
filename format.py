
from PIL import Image
import glob
import cv2
import random
import torchvision.transforms as T
import torch

data_paths = glob.glob("./aligned/*")
data_paths.sort()

training_proportion = 0.9
# print(data)

# def getFname(path):
#     return path.split('/')[-1]
data = []
for index in range(0, len(data_paths),2):
    ground = Image.open(data_paths[index])
    flat = Image.open(data_paths[index+1])
    data.append((ground, flat))
    
print(len(data))

training_samples = round(training_proportion * len(data))
random.shuffle(data)

training_data = data[:training_samples]
test_data = data[training_samples:]


def pad_images(inp, out, num_paddings):
    padding_values = random.sample(range(3, 30), num_paddings)
    padded_inp = []
    for img in inp:
        padded_inp.extend([T.Pad(padding=padding)(img) for padding in padding_values])
    padded_out = []
    for img in out:
        padded_out.extend([T.Pad(padding=padding)(img) for padding in padding_values])

    return padded_inp, padded_out

def affine_images(inp, out, num_affines):
    random_seed = random.randint(0, 1000)
    affine = T.RandomAffine(degrees=(-20, 20), translate=(0, 0.12), scale=(0.7, 1))
    affined_inp = []
    torch.manual_seed(random_seed)
    for img in inp:
        affined_inp.extend([affine(img) for _ in range(num_affines)])
        
    torch.manual_seed(random_seed)
    affined_out = []
    for img in out:
        affined_out.extend([affine(img) for _ in range(num_affines)])
    return affined_inp, affined_out

def mutliplyImages(inp, out):
    inp, out = pad_images(inp, out, 3)
    inp, out = affine_images(inp, out, 6)
    # print(len(inp), len(out))
    return inp, out


extended_training_data = training_data[:]

for ground, flat in training_data:
    exp_ground, exp_flat = mutliplyImages([ground], [flat])
    extended_training_data.extend(zip(exp_ground, exp_flat))

print(len(extended_training_data))

import os
def saveData(data, inp_dir, out_dir):
    index = 1
    for (inp, out) in data:
        inp.save(os.path.join(inp_dir, f"{index}.png"))
        out.save(os.path.join(out_dir, f"{index}.png"))
        index+=1
        

saveData(extended_training_data, "formatted/in/train", "formatted/out/train")

saveData(test_data, "formatted/in/test", "formatted/out/test")