import time
import torch
import torch.nn as nn
import torchvision
import numpy as np
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, random_split, Subset
from torchvision import datasets
from torchvision.datasets import ImageFolder
import torchvision.transforms as tt
from torchvision.utils import make_grid
import matplotlib.pyplot as plt
from matplotlib.image import imread
import os
import random
from tqdm import tqdm
from PIL import Image #not sure if this one is necessary
from CNN import CNN


def Find_Average_Image_Dimension():
    width = 0
    height = 0
    number_Of_Images = 0
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "thecarconnectionpicturedataset"))
    for file in tqdm(os.listdir(directory)):
        filepath = os.path.join(directory,file)
        img = Image.open(filepath) # Opens the Image
        number_Of_Images +=1
        width += img.size[0]
        height += img.size[1]
    width = width/number_Of_Images
    height = height/ number_Of_Images
    return (width,height)


# Loads the dataset from the file location
def load_dataset( crop_width, crop_height, batch_size = 32, train=True):
    dataset = []
    batch_counter = 0
    batch = []
    feature_set = []
    counter = 0
    # TODO Add file size changes
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "thecarconnectionpicturedataset"))
    for file in tqdm(os.listdir(directory)):
        filepath = os.path.join(directory,file)
        img = Image.open(filepath) # Opens the Image

        # Crops the image to size new_width x new_height
        width = img.size[0]
        height = img.size[1]
        left = (width - crop_width)/2
        top = (height - crop_height)/2
        right = left+crop_width
        bottom = top+crop_height

        # Cropped image of above dimension
        # (It will not change original image)
        img = img.crop((left, top, right, bottom))
        img = np.asarray(img)

        img_features = file.split("_") # Gets the features from the file name
        feature_set.append(img_features)

        if(counter > 1000):
            break
        else:
            counter+=1
        if batch_counter < batch_size:
            batch.append(img)
            batch_counter = batch_counter + 1
        else:
            dataset.append(np.array(batch))
            batch = []
            batch_counter = 0

    return np.array(dataset)


def plot_image(image, crop_width, crop_height):
    image = image.reshape(-1,crop_height,crop_width,3)
    plt.imshow(image[0])
    plt.show()
    return

#Option1: 
#Also variable methods when working with GPU, would look into that
model = CNN()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
# direct = os.path.realpath(os.path.join(os.path.dirname("ModelState.pt"), "..", "SavedStates"))
#save model
torch.save(model.state_dict(), "../SavedStates/ModelState.pt")
#load entire model
model.load_state_dict(torch.load("../SavedStates/ModelState.pt"))
model.eval()

#Option2: 
#Saving & Loading a General Checkpoint for Inference and/or Resuming Training
#https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-loading-a-general-checkpoint-for-inference-and-or-resuming-training 
    #Saving
# torch.save({
#             'epoch': epoch,
#             'model_state_dict': model.state_dict(),
#             'optimizer_state_dict': optimizer.state_dict(),
#             'loss': loss
#             }, "../SavedStates/ModelState.pt")

    #Loading
# checkpoint = torch.load("../SavedStates/ModelState.pt")
# model.load_state_dict(checkpoint['model_state_dict'])
# optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
# epoch = checkpoint['epoch']
# loss = checkpoint['loss']
# model.eval()
# # - or -
# model.train()


crop_width = 300  # Average Width of the cropped image is 320
crop_height = 210  # Average Height of the cropped image is 230
dataset = load_dataset(crop_width, crop_height, batch_size=32, train=True)

ex_image = dataset[random.randint(0, 10)]
print("image shape:", ex_image.shape)
plot_image(ex_image,crop_width=crop_width,crop_height=crop_height)


####################################################
#Create model


#training loop


#save model states



#test on test set



#Create graph(s)

#Done for the first milestone

#################################################
