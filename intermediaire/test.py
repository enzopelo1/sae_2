import cv2
import numpy as np

# Charger l'image astronomique
image_astronomique = cv2.imread('./fichiers ressource-20231023/barnard_stacked_gradient.png')

# Convertir l'image en niveaux de gris pour faciliter le traitement
gray_image = cv2.cvtColor(image_astronomique, cv2.COLOR_BGR2GRAY)

# Appliquer un seuil pour détecter la pollution lumineuse (vous devrez ajuster ce seuil)
_, pollution_mask = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

# Inverser le masque pour détecter la région sans pollution lumineuse
non_pollution_mask = cv2.bitwise_not(pollution_mask)

# Assombrir la région sans pollution lumineuse
image_astronomique[non_pollution_mask > 0] = image_astronomique[non_pollution_mask > 0] * 0.3

# Enregistrer l'image résultante
cv2.imwrite('image_mis_en_evidence.jpg', image_astronomique)
