"""
PhotoFiltre - Simple Image Processing App

This Python application, PhotoFiltre, provides basic image processing functionalities.
It uses Tkinter for the graphical user interface, featuring an interface designed for a screen resolution of 1920x1080.
Images are preferably in the format 1600x900.
Before runing the application, you need to load every files.

Features:
- Black and White Conversion: Converts the image to grayscale.
- Negative Effect: Generates the negative of the image.
- Brightness Adjustment: Increases the brightness of the image.
- Image Rotation: Rotates the image by 180 degrees.
- Blur Effect: Applies a blur effect to the image.
- Monochromatic Effect: Emphasizes a color (Red, Green, or Blue).

Usage:
1. Run the application and choose an image from the provided options or import your own.
2. Use buttons to apply different effects.
3. Save the processed image or reset to the original state.
4. Exit the application after saving or discard changes.

Author: MARIE Camil, LHERMITTE Léo
Date: 17/01/2024
"""


#tkinter
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
#PIL
from PIL import ImageTk, Image
#filedialog
from tkinter import filedialog
#numpy
import numpy as np
from scipy.ndimage import convolve

# commandes couleurs
#b&w
def grey_lvl(windo):
    global img_used
    data = img_used.getdata()  # Obtient les données de l'image
    new_data = []
    for pixel in data:
        r, g, b = pixel[0], pixel[1], pixel[2]
        grey_level = (r + g + b) // 3
        new_data.append((grey_level, grey_level, grey_level))
    newimg.putdata(new_data)  # Place les nouvelles données dans l'image
    file_name_new="Nouveau.png"
    newimg.save(file_name_new)
    name_img= ImageTk.PhotoImage(Image.open(file_name_new))
    name_shown= tk.Label(windo, image=name_img)
    name_shown.photo=name_img
    name_shown.place(x=20,y=110)
    img_used=newimg

#negative
def negative_img(windo):
    global img_used
    data = img_used.getdata()
    new_data = []

    for pixel in data:
        r, g, b = pixel[0], pixel[1], pixel[2]
        new_data.append((255 - r, 255 - g, 255 - b))

    newimg.putdata(new_data)
    file_name_new="Nouveau.png"
    newimg.save(file_name_new)
    name_img= ImageTk.PhotoImage(Image.open(file_name_new))
    name_shown= tk.Label(windo, image=name_img)
    name_shown.photo=name_img
    name_shown.place(x=20,y=110)
    img_used=newimg

#complete rotation
def rotate(windo):
    global img_used
    newimg = img_used.rotate(-180)
    file_name_new="Nouveau.png"
    newimg.save(file_name_new)
    name_img= ImageTk.PhotoImage(Image.open(file_name_new))
    name_shown= tk.Label(windo, image=name_img)
    name_shown.photo=name_img
    name_shown.place(x=20,y=110)
    img_used=newimg


#scrolling menu and monochromatic effect

def unicolor(event,windo,menu):
    global img_used
    data = img_used.getdata()
    new_data = []
    for pixel in data:
        r, g, b = pixel[0], pixel[1], pixel[2]

        # Change target color component, others to zero
        if menu.get() == 'Red':
            new_data.append((r-30, 0, 0))
        elif menu.get() == 'Green':
            new_data.append((0, g-30, 0))
        elif menu.get() == 'Blue':
            new_data.append((0, 0, b-30))
        else:
            print("ça marche pas")

    newimg.putdata(new_data)
    file_name_new="Nouveau.png"
    newimg.save(file_name_new)
    name_img= ImageTk.PhotoImage(Image.open(file_name_new))
    name_shown= tk.Label(windo, image=name_img)
    name_shown.photo=name_img
    name_shown.place(x=20,y=110)
    img_used=newimg


# Change brightness
def lightless_img(windo):
    global img_used
    data = img_used.getdata()
    new_data = []

    for pixel in data:
        r, g, b = int(pixel[0] * coef), int(pixel[1] * coef), int(pixel[2] * coef)
        r = min(r, 255)
        g = min(g, 255)
        b = min(b, 255)
        new_data.append((r, g, b))

    newimg.putdata(new_data)
    file_name_new="Nouveau.png"
    newimg.save(file_name_new)
    name_img= ImageTk.PhotoImage(Image.open(file_name_new))
    name_shown= tk.Label(windo, image=name_img)
    name_shown.photo=name_img
    name_shown.place(x=20,y=110)
    img_used=newimg

#blur effect
def blured(windo,k):
    global img_used
    img_array = np.array(img_used)
    kernel = np.ones((k, k)) / k**2  # 5x5 mean filter kernel
    blurred_array = np.zeros_like(img_array)
    for c in range(img_array.shape[2]):  # Loop over color channels
        blurred_array[:, :, c] = convolve(img_array[:, :, c], kernel, mode='constant', cval=0.0)

    newimg=Image.fromarray(np.uint8(blurred_array))
    file_name_new="Nouveau.png"
    newimg.save(file_name_new)
    name_img= ImageTk.PhotoImage(Image.open(file_name_new))
    name_shown= tk.Label(windo, image=name_img)
    name_shown.photo=name_img
    name_shown.place(x=20,y=110)
    img_used=newimg

#commands

def import_img():
    window.filename=filedialog.askopenfilename(initialdir='/', title='Select a file', filetypes=[("png files","*.png")])
    fenetre2(window.filename)


def exit(fenetre):
    window.deiconify()
    fenetre.withdraw()
    save_file()


def reload(windo,name):
    global img_used
    img_used=Image.open(name).convert('RGB')
    img_used=img_used.resize((1600,920))
    img_used_tkinter=ImageTk.PhotoImage(img_used)
    image_edit= tk.Label(windo, image=img_used_tkinter)
    image_edit.photo=img_used_tkinter
    image_edit.place(x=20,y=110)

def save_file():
    global img_used
    file_location=filedialog.asksaveasfilename(defaultextension='png',filetypes=[("png files",".png"),("All files",".*")])
    if file_location:
        img_used.save(file_location)
        showimage=messagebox.askyesno("PhotoFiltre","Your image was succesfully saved ! Do you want to see it ?")
        print(showimage)
        if showimage:
            img_used.show()

def turn_off(windo,fenetre_sec):
    if windo==fenetre_sec:
        windo.withdraw()
        window.deiconify()
    else:
        windo.destroy()


#app
def fenetre2(file):
    global img_used
    img_used=file
    img_used=Image.open(img_used).convert('RGB')
    img_used=img_used.resize((1600,920))
    name=ImageTk.PhotoImage(img_used)
    fenetre_app=tk.Toplevel()
    fenetre_app.title('PhotoFiltre')
    fenetre_app.geometry("1920x1080")
    fenetre_app.minsize(1920,1080)
    fenetre_app.iconbitmap("PhotoFiltre-logo (2).ico")
    fenetre_app.config(background="#0A0433")
    fenetre_app.attributes('-topmost',True)
    titre= tk.Label(fenetre_app, image=FotoPhiltre_file, bg="#0A0433", bd=0)
    titre.place(x=710,y=1)
    window.withdraw()
    quit= tk.Button(fenetre_app, text='Save/Leave',font=('Times',30,), command=lambda:exit(fenetre_app))
    quit.place(x=1660,y=890)
    reinitialiser=tk.Button(fenetre_app, text="Reset",font=("Helvetica", 25), bg='black',fg='white',activebackground='cyan',bd=0, command=lambda:reload(fenetre_app, file))
    reinitialiser.place(x=1700,y=800)
    image_edit= tk.Label(fenetre_app, image=name)
    image_edit.photo=name
    image_edit.place(x=20,y=110)
    bandw= tk.Button(fenetre_app, text= "Black and White", font=('Helvetica', 25), activeforeground="black", activebackground="white", bg="black", fg='white',bd=0, command=lambda:grey_lvl(fenetre_app))
    bandw.place(x=1640,y=120)
    negative= tk.Button(fenetre_app, text="Negative", font=('Helvetica',25), activeforeground="black",activebackground='green',bg='navy',fg='white',bd=0,command=lambda:negative_img(fenetre_app))
    negative.place(x=1680,y=210)
    lightless= tk.Button(fenetre_app, text="Brightness ++", font=('Helvetica',25), activeforeground='white',bg='yellow',fg="black",bd=0, command=lambda:lightless_img(fenetre_app))
    lightless.place(x=1655,y=300)
    rotated=tk.Button(fenetre_app, text='Rotate', font=('Helvetica', 25), fg='black', activebackground='red',bg='#6e0801',bd=0, command=lambda:rotate(fenetre_app))
    rotated.place(x=1700,y=390)
    blur=tk.Button(fenetre_app, text='Blur', font=('Helvetica',25), fg='grey', activeforeground='black',bg='#e3e3e3',bd=0,command=lambda:blured(fenetre_app,10))
    blur.place(x=1710,y=480)
    listecouleurs=["Red",'Green',"Blue"]
    menu_deroulant=ttk.Combobox(fenetre_app, values=listecouleurs, width=30, height=10)
    menu_deroulant.bind("<<ComboboxSelected>>", lambda event :unicolor(event,fenetre_app,menu_deroulant))
    menu_deroulant.set("Monochromatic")
    menu_deroulant.place(x=1660,y=570)
    quit1=tk.Button(fenetre_app,image=quit_file,bd=0,command=lambda:turn_off(fenetre_app,fenetre_app),bg="#0A0433")
    quit1.place(x=1800,y=15)

#color variables
newimg=Image.new("RGB",(1600,920))
coef=3
l = 1600
L = 920


#main window

fenetresec="fenetre_app"
window = tk.Tk()
window.title("FotoPhiltre Menu")
window.geometry("1920x1080")
window.minsize(1920,1080)
window.iconbitmap("PhotoFiltre-logo (2).ico")
window.config(background="#0A0433")
FotoPhiltre_file=tk.PhotoImage(file="titre.png")
title= tk.Label(window, image=FotoPhiltre_file, bg="#0A0433", bd=0)
title.pack()

#pictures

oppenheimer_file= tk.PhotoImage(file='oppenheimer.png')
oppenheimer_button= ttk.Button(window, image=oppenheimer_file, command=lambda:fenetre2('oppenheimer_resize.png'))
oppenheimer_button.place(y=120,x=25)

fight_club_file= tk.PhotoImage(file='fight_club.png')
fight_club_button= ttk.Button(window, image=fight_club_file, command=lambda:fenetre2("fight_club_resize.png"))
fight_club_button.place(y=120,x=975)

interstellar_file= tk.PhotoImage(file='interstellar.png')
interstellar_button= ttk.Button(window, image=interstellar_file,command=lambda:fenetre2("interstellar_resize.png"))
interstellar_button.place(y=580,x=25)

shrek_file= tk.PhotoImage(file='shrek.png')
shrek_button= ttk.Button(window, image=shrek_file, command=lambda:fenetre2("shrek_resize.png"))
shrek_button.place(y=580,x=975)

#pictures importation
import_image=tk.Button(window, text='Import an image', bd=0, fg='black', bg='white', font=('Helvetica',30), command=lambda:import_img())
import_image.place(x=50,y=20)

#quit
quit_file=tk.PhotoImage(file='quit (1).png')
quit=tk.Button(window,image=quit_file,bd=0,command=lambda:turn_off(window,fenetresec),bg="#0A0433")
quit.place(x=1800,y=15)



window.mainloop()