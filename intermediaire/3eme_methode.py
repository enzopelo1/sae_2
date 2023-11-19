import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def equalize_histogram(image_path, output_folder):
    # Chargement de l'image astronomique
    image_astronomique = cv2.imread(image_path)

    # Conversion en niveaux de gris
    gray_image = cv2.cvtColor(image_astronomique, cv2.COLOR_BGR2GRAY)

    # Égalisation d'histogramme
    equalized_image = cv2.equalizeHist(gray_image)

    # Enregistrement de l'image résultante dans un dossier spécifique
    output_path = os.path.join(output_folder, 'image_egalisation_histogramme.jpg')
    cv2.imwrite(output_path, equalized_image)

    # Affichage de l'image résultante
    display_image(equalized_image)

def display_image(image):
    # Création d'une fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("Image Astronomique Modifiée")
    fenetre.attributes('-fullscreen', True) 
    
    # Redimensionnement de l'image pour l'affichage
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # Convertir en RGB pour l'affichage
    image = Image.fromarray(image)
    image = image.resize((1000, 700))
    photo = ImageTk.PhotoImage(image=image)

    # Création d'un label pour afficher l'image
    label = ttk.Label(fenetre, image=photo)
    label.pack()

    fenetre.mainloop()

if __name__ == "__main__":
    # Créer un dossier pour enregistrer les images résultantes
    output_folder = 'images_resultantes'
    os.makedirs(output_folder, exist_ok=True)

    # Exécuter la méthode avec le dossier de sortie spécifié
    equalize_histogram('fichiers ressource-20231023/barnard_stacked_gradient.png', output_folder)
