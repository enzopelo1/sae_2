import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMenuBar, QAction
from PyQt5.QtGui import QPixmap, QImage, QImageReader, QImageWriter
from PyQt5.QtCore import Qt
import cv2

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traitement d'images astronomiques")
        self.setGeometry(100, 100, 1024, 600)

        # Créer une zone centrale pour afficher les images
        self.central_widget = QGraphicsView(self)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: black; color: white;")

        self.scene = QGraphicsScene()
        self.central_widget.setScene(self.scene)

        self.text_label = QLabel("Traitement d'une image astronomique", self)
        self.text_label.setGeometry(485, 200, 300, 30)
        
        # Créer une barre de menu
        menubar = self.menuBar()
        
        # Créer un menu "Fichier"
        file_menu = menubar.addMenu("Fichier")
        
        # Ajouter une action pour charger une image
        load_action = QAction("Charger une image", self)
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)
        
        # Ajouter une action pour soustraire le gradient
        subtract_action = QAction("Soustraire le gradient", self)
        subtract_action.triggered.connect(self.subtract_gradient)
        file_menu.addAction(subtract_action)

        # Variables pour stocker les images
        self.image = None
        self.processed_image = None

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionnez l'image astronomique", "", "Images (*.jpg *.png *.bmp);;Tous les fichiers (*)", options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            if self.image is not None:
                self.update_display()
                
    def subtract_gradient(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionnez le fichier de gradient", "", "Images (*.jpg *.png *.bmp);;Tous les fichiers (*)", options=options)
        if file_name:
            gradient = cv2.imread(file_name)
            if gradient is not None:
                self.processed_image = cv2.subtract(self.image, gradient)
                self.update_display(self.processed_image)

    def update_display(self, img=None):
        if img is None:
            img = self.image

        # Redimensionner l'image pour qu'elle soit plus petite
        if img is not None:
            height, width, channel = img.shape
            max_height = self.central_widget.height()  # Hauteur maximale de la fenêtre
            max_width = self.central_widget.width() // 2  # Largeur maximale de la moitié de la fenêtre

            if height > max_height or width > max_width:
                scale_factor = min(max_width / width, max_height / height)
                img = cv2.resize(img, (int(scale_factor * width), int(scale_factor * height)))

            bytes_per_line = 3 * img.shape[1]
            q_image = QImage(img.data, img.shape[1], img.shape[0], bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()
            self.scene.addItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.showMaximized()  # Afficher la fenêtre en plein écran
    window.show()
    sys.exit(app.exec_())
