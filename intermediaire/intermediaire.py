import cv2
import numpy as np

from PIL import Image, ImageTk


def main():
    # Chargement d'une image astronomique
    image_astronomique = cv2.imread(
        'fichiers ressource-20231023/barnard_stacked_gradient.png')

    # Convertion d'une image en niveaux de gris pour faciliter le traitement
    gray_image = cv2.cvtColor(image_astronomique, cv2.COLOR_BGR2GRAY)

    # Appliquage d'un seuil pour détecter la pollution lumineuse
    _, pollution_mask = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Inversion du masque pour détecter la région sans pollution lumineuse
    non_pollution_mask = cv2.bitwise_not(pollution_mask)

    # Assombrissement de la région sans pollution lumineuse
    image_astronomique[non_pollution_mask >
                       0] = image_astronomique[non_pollution_mask > 0] * 0.1

    # Enregistrement de l'image résultante
    cv2.imwrite('image_mis_en_evidence.jpg', image_astronomique)


if __name__ == "__main__":
    main()


# qu'est ce qu'on a appris
