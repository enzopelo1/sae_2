import cv2
import numpy as np

def darken_light_pollution(image_path, output_path, block_size=15, darken_factor=0.7):
    # Charger l'image en niveaux de gris
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculer le Dark Channel Prior
    dark_channel = cv2.erode(gray_image, np.ones((block_size, block_size), np.uint8))

    # Estimer l'intensité de l'éclairage global (Atmospheric Light)
    atmospheric_light = np.percentile(image, 99)

    # Calculer la transmission
    transmission = 1 - (dark_channel / atmospheric_light)

    # Assombrir les zones affectées par la pollution lumineuse
    darkened_image = image.copy()
    for i in range(3):
        darkened_image[:, :, i] = image[:, :, i] * (1 - transmission * darken_factor)

    # Limiter les valeurs des pixels entre 0 et 255
    darkened_image = np.clip(darkened_image, 0, 255).astype(np.uint8)

    # Enregistrer l'image assombrie
    cv2.imwrite(output_path, darkened_image)
    print(f"Image avec les zones de pollution lumineuse assombries enregistrée sous {output_path}")

# Exemple d'utilisation de la fonction
input_image_path = 'fichiers ressource-20231023/barnard_stacked_gradient.png'
output_image_path = "image_sans_pollution_assombrie.jpg"
darken_light_pollution(input_image_path, output_image_path)
