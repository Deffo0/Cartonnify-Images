import PIL
import cv2  # for image processing
import easygui  # to open the filebox
import numpy as np  # to store image
import imageio  # to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image


def upload():
    image_path = easygui.fileopenbox()
    cartoonify(image_path)





def cartoonify(image_path):
    # specify the width and the height of the image
    image = PIL.Image.open(image_path)
    image.show()
    width, height = image.size
    # read the image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # confirm that image is chosen
    if original_image is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    resized1 = cv2.resize(original_image, (width, height))

    # converting an image to grayscale
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    resized2 = cv2.resize(gray_scale_image, (width, height))

    # applying median blur to smoothen an image
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 9)
    resized3 = cv2.resize(smooth_gray_scale, (width, height))

    # retrieving the edges for cartoon effect
    # by using thresholding technique
    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 3, 3)

    resized4 = cv2.resize(get_edge, (width, height))

    # applying bilateral filter to remove noise
    # and keep edge sharp as required
    color_image = cv2.bilateralFilter(original_image, 5, 300, 300)
    resized5 = cv2.resize(color_image, (width, height))

    # masking edged image with our "BEAUTIFY" image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)

    resized6 = cv2.resize(cartoon_image, (width, height))

    # Plotting the whole transition
    images = [resized1, resized2, resized3, resized4, resized5, resized6]
    fig, axes = plt.subplots(3, 2, figsize=(10, 10), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.imshow(resized6, cmap='gray')
    save1 = Button(top, text="Cartoonify & Save ur image", command=lambda: save(resized6, image_path), padx=10, pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save1.pack(side=TOP, pady=50)

    plt.show()


def save(resized6, image_path):
    # saving an image using imwrite()
    new_name = "cartoonified_Image"
    path1 = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(resized6, cv2.COLOR_RGB2BGR))
    image = PIL.Image.open(path)
    image.show()
    I = "Image saved by name " + new_name + " at " + path
    tk.messagebox.showinfo(title=None, message=I)


if __name__ == '__main__':
    top = tk.Tk()
    top.geometry('400x400')
    top.title('Cartoonify Your Image !')
    top.configure(background='white')
    label = Label(top, background='#CDCDCD', font=('calibri', 10, 'bold'))
    upload = Button(top, text="Select an Image", command=upload, padx=10, pady=5)
    upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    upload.pack(side=TOP, pady=50)
    top.mainloop()
