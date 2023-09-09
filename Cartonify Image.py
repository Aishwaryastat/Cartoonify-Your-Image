# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 14:43:50 2023

@author: pcc
"""
import cv2
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import easygui 
import imageio
import sys 
import os 
import tkinter as tk 
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

# Making the main window
top=tk.Tk()
top.geometry("400x400")
top.title("Cartoonify Your Image !")
top.configure(background="white")
label=Label(top,background="#CDCDCD",font=("calibri",20,"bold"))


# Building a file box to choose a image 
def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)
    
def cartoonify(ImagePath):
    # Store Image
    originalimage=cv2.imread(ImagePath)
    originalimage=cv2.cvtColor(originalimage,cv2.COLOR_BGR2RGB)
    
    if originalimage is None:
        print("Can not find any image, Choose appropriate Image.")
        sys.exit()
        
    resize1=cv2.resize(originalimage,(960,540))
    
    #plt.imshow(resize1,cmap="gray")   
    # Tansform and image to grayscale
    grayScaleImage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2GRAY)
    resize2=cv2.resize(grayScaleImage,(960,540))
    #plt.imshow(resize2,cmap="gray")
    
    # Smoothing a grayscale image 
    # apply mendian blur to smoothen an image 
    
    smoothgray=cv2.medianBlur(grayScaleImage, 5)
    resize3=cv2.resize(smoothgray,(960,540))
    
    #plt.imshow(resize3,cmap="gray")
    
    # Retriving the edges of an image
    # retreving edges using threshold technique
    getedge= cv2.adaptiveThreshold(smoothgray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                   cv2.THRESH_BINARY, 9, 9)
    resize4=cv2.resize(getedge,(960,540))
    #plt.imshow(resize4,cmap="gray")
    
    # Preparing a mask image 
    # applying bilateral filter to remove the noise
    
    colorimage=cv2.bilateralFilter(originalimage,9,300,300)
    resize5=cv2.resize(colorimage,(960,540))
    #plt.imshow(resize5,cmap="gray")
    
    # Giving a cartoon effect
    cartoonimage=cv2.bitwise_and(colorimage,colorimage,mask=getedge)
    resize6=cv2.resize(cartoonimage,(960,540))
    #plt.imshow(resize6, cmap="gray")
    
    # Plotting all the transitions together
    images=[resize1,resize2,resize3,resize4,resize5,resize6]
    fig,axes=plt.subplots(3,2,figsize=(8,8),subplot_kw={'xticks':[],'yticks':[]},gridspec_kw=dict(hspace=0.1,wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i],cmap="gray")
    # Making a save button in main window
    save1=Button(top,text="Save cartoon image", command=lambda: save(ImagePath, resize6),padx=30,pady=5)
    save1.configure(background="#364156",foreground="white",font=('calibri',10,"bold"))
    save1.pack(side=TOP,pady=50)
    plt.show()
    
    
# Functionally of save button

def save(ImagePath, resize6):
    newname = "Cartoonified_image"
    path1 = os.path.dirname(str(ImagePath))  # Convert ImagePath to a string
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newname + extension)
    cv2.imwrite(path, cv2.cvtColor(resize6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newname + " at " + path
    tk.messagebox.showinfo(title=None, message=I)
    
    
# Making cartoonify button in main window

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background="#364156",foreground="white",font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

# Main function to build the tkinter window
top.mainloop()