import cv2
import numpy as np

# Chargement de l'image en niveaux de gris
image_path = "fichiers ressource-20231023/barnard_stacked_gradient.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
gradient = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
gradient = cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX)
gradient = np.uint8(gradient)

# Enregistrement de l'image avec le gradient élevé
output_path = "images_resultantes/image_resultat.jpg"
cv2.imwrite(output_path, gradient)

print(f"Image résultante enregistrée à : {output_path}")
