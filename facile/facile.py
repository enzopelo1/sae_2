import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

# Déclarer la variable canvas en dehors des fonctions
canvas = None

# Fonction pour charger une image
def charger_image():
    global canvas  # Utilisez la variable canvas globale
    file_path = filedialog.askopenfilename(title="Sélectionnez l'image astronomique")
    if file_path:
        image = Image.open(file_path)
        image = image.resize((700, 400))  # Redimensionne l'image
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo
        global image_to_process
        image_to_process = cv2.imread(file_path)

# Fonction pour soustraire le gradient de l'image
def soustraire_gradient():
    if image_to_process is not None:
        gradient_path = filedialog.askopenfilename(title="Sélectionnez le fichier de gradient")
        if gradient_path:
            gradient = cv2.imread(gradient_path)
            if gradient is not None:
                image_soustraite = cv2.subtract(image_to_process, gradient)

                # Afficher les images côte à côte dans le canevas
                canvas.delete("all")

                # Convertir les images OpenCV en images PIL
                image_to_display = Image.fromarray(cv2.cvtColor(image_to_process, cv2.COLOR_BGR2RGB))
                image_soustraite_display = Image.fromarray(cv2.cvtColor(image_soustraite, cv2.COLOR_BGR2RGB))

                # Afficher l'image d'origine à gauche
                image_to_display.thumbnail((350, 400))
                image_to_display = ImageTk.PhotoImage(image_to_display)
                canvas.create_image(10, 10, anchor=tk.NW, image=image_to_display)

                # Afficher l'image soustraite à droite
                image_soustraite_display.thumbnail((350, 400))
                image_soustraite_display = ImageTk.PhotoImage(image_soustraite_display)
                canvas.create_image(370, 10, anchor=tk.NW, image=image_soustraite_display)

                canvas.image = image_to_display, image_soustraite_display

# Configuration de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Traitement d'images astronomiques")

# Obtenir la taille de l'écran
screen_width = fenetre.winfo_screenwidth()
screen_height = fenetre.winfo_screenheight()

# Configurer la taille de la fenêtre pour occuper toute la taille de l'écran
fenetre.geometry(f"{screen_width}x{screen_height}")
fenetre.configure(bg="black")
# Création d'un bouton pour charger l'image
charger_bouton = tk.Button(fenetre, text="Charger une image", command=charger_image, bg="black", fg="white")
charger_bouton.pack()

# Création d'un bouton pour soustraire le gradient
soustraire_bouton = tk.Button(fenetre, text="Soustraire le gradient", command=soustraire_gradient, bg="black", fg="white")
soustraire_bouton.pack()

# Création d'un canevas pour afficher les images côte à côte
canvas = tk.Canvas(fenetre, width=720, height=400, bg="black")
canvas.pack()

image_to_process = None

fenetre.mainloop()
