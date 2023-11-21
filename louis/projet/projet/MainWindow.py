import cv2
import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


class Fenêtre(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STARLISA")
        self.setWindowIcon(QIcon('icon.png'))
        self.setMouseTracking(True)
        self.showMaximized()

        self.imageOpen = False

        self.scrollArea = QScrollArea()

        self.scale_factor = 1.0
        self.label = QLabel("")
        self.scrollArea.setWidget(self.label)
        self.label.setScaledContents(True)
        self.label.adjustSize()
        self.image = ''

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setCentralWidget(self.scrollArea)

        # Create buttons for zoom, filters, and method 2
        self.openImage = QPushButton(QIcon('nouveau-fichier.png'), "")
        self.openImage.setMaximumSize(30, 30)
        self.openImage.setToolTip('Open Image')

        self.closeImageButton = QPushButton(QIcon('fermer.png'), "")
        self.closeImageButton.setMaximumSize(30, 30)
        self.closeImageButton.setToolTip('Close Image')

        self.zoom_in_button = QPushButton(QIcon('zoom.png'), "")
        self.zoom_in_button.setMaximumSize(30, 30)
        self.zoom_in_button.setToolTip('Zoom in')

        self.zoom_out_button = QPushButton(QIcon('zoom_out.png'), "")
        self.zoom_out_button.setMaximumSize(30, 30)
        self.zoom_out_button.setToolTip('Zoom out')

        self.undo_button = QPushButton(QIcon('undo_arrow.png'), "")
        self.undo_button.setMaximumSize(30, 30)
        self.undo_button.setToolTip('Undo')

        self.redo_button = QPushButton(QIcon('redo_arrow.png'), "")
        self.redo_button.setMaximumSize(30, 30)
        self.redo_button.setToolTip('Redo')

        self.filtersButton = QPushButton(QIcon('couleurs.png'), "")
        self.filtersButton.setMaximumSize(30, 30)
        self.filtersButton.setToolTip('Add filters Method 1')

        self.method2Button = QPushButton(QIcon('couleurs.png'), "")
        self.method2Button.setMaximumSize(30, 30)
        self.method2Button.setToolTip('Add filters Method 2')

        self.resetSizeOfImage = QPushButton(QIcon('minimiser.png'), "")
        self.resetSizeOfImage.setMaximumSize(30, 30)
        self.resetSizeOfImage.setToolTip('Reset image size')

        self.gradientFilterButton = QPushButton(QIcon('gradient.png'), "")
        self.gradientFilterButton.setMaximumSize(30, 30)
        self.gradientFilterButton.setToolTip('Apply gradient filter')

        # Add an expanding spacer
        spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Connect signals to slots
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.openImage.clicked.connect(self.open)
        self.closeImageButton.clicked.connect(self.close)
        self.resetSizeOfImage.clicked.connect(self.reset_zoom)
        self.filtersButton.clicked.connect(self.method1)
        self.method2Button.clicked.connect(self.method2)
        self.gradientFilterButton.clicked.connect(self.subtract_gradient)

        # Create a QHBoxLayout for the buttons
        self.toolsLayout = QHBoxLayout()
        self.toolsLayout.addWidget(self.openImage)
        self.toolsLayout.addWidget(self.closeImageButton)
        self.toolsLayout.addWidget(self.undo_button)
        self.toolsLayout.addWidget(self.redo_button)
        self.toolsLayout.addWidget(self.zoom_in_button)
        self.toolsLayout.addWidget(self.zoom_out_button)
        self.toolsLayout.addWidget(self.resetSizeOfImage)
        self.toolsLayout.addWidget(self.filtersButton)
        self.toolsLayout.addWidget(self.method2Button)
        self.toolsLayout.addWidget(self.gradientFilterButton)
        self.toolsLayout.addSpacerItem(spacer)

        # Create a QMenu bar containing the tools (at the top)
        self.menu_bar = QMenuBar()

        # File menu
        self.menu_fichier = self.menu_bar.addMenu("File")
        self.action_ouvrir_image = self.menu_fichier.addAction("Open Image")
        self.action_ouvrir_image.triggered.connect(self.open)
        self.action_enregistrer_image = self.menu_fichier.addAction(
            "Save Image")
        self.action_exporter_image = self.menu_fichier.addAction(
            "Export Image")
        self.action_fermer_image = self.menu_fichier.addAction("Close Image")
        self.action_quitter = self.menu_fichier.addAction("Quit")

        # Edit menu
        self.menu_édition = self.menu_bar.addMenu("Edit")
        self.action_undo = self.menu_édition.addAction("Undo")
        self.action_redo = self.menu_édition.addAction("Redo")
        self.action_zoomer = self.menu_édition.addAction("Zoom +")
        self.action_zoomer.triggered.connect(self.zoom)
        self.action_dézoomer = self.menu_édition.addAction("Zoom -")
        self.action_dézoomer.triggered.connect(self.zoom_out)

        # Filters submenu
        self.menu_filtres = QMenu("Filters")
        self.action_gradient_1 = self.menu_filtres.addAction("Gradient 1")
        self.action_gradient_2 = self.menu_filtres.addAction("Gradient 2")
        self.menu_édition.addMenu(self.menu_filtres)

        # Help menu
        self.menu_aide = self.menu_bar.addMenu("Help")

        self.setMenuBar(self.menu_bar)

        # Set up the main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.toolsLayout)
        self.main_layout.addWidget(self.scrollArea)

        # Set up the footer layout
        self.footerLayout = QHBoxLayout()
        self.pathImageOpen = QLabel("")
        self.testtitle = QLabel("STARLISA © - version 1.0")
        self.footerLayout.addWidget(self.pathImageOpen)
        self.footerLayout.addSpacerItem(spacer)
        self.footerLayout.addWidget(self.testtitle)
        self.main_layout.addLayout(self.footerLayout)

        # Use a central widget to set the main layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def zoom_in(self):
        self.zoom_in, self.zoom_out, self.reset_zoom = True, False, False
        self.zoom()

    def zoom_out(self):
        self.zoom_in, self.zoom_out, self.reset_zoom = False, True, False
        self.zoom()

    def reset_zoom(self):
        self.zoom_in, self.zoom_out, self.reset_zoom = False, False, True
        self.zoom()

    def close(self):
        self.label.clear

    def zoom(self):
        if (self.scale_factor > 3.0 and self.zoom_in) or (self.scale_factor < 0.3 and self.zoom_out):
            return
        try:
            if self.zoom_in:
                frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                image = QImage(
                    frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(image))
                self.scale_factor *= 1.1
                newScaleImage = self.scale_factor * self.label.pixmap().size()
                self.label.resize(newScaleImage)
                self.label.setPixmap(QPixmap.fromImage(image).scaled(
                    self.label.size(), QtCore.Qt.IgnoreAspectRatio,
                    QtCore.Qt.SmoothTransformation))
            elif self.zoom_out:
                frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                image = QImage(
                    frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(image))
                self.scale_factor /= 1.1
                newScaleImage = self.scale_factor * self.label.pixmap().size()
                self.label.resize(newScaleImage)
                self.label.setPixmap(QPixmap.fromImage(image).scaled(
                    self.label.size(), QtCore.Qt.IgnoreAspectRatio,
                    QtCore.Qt.SmoothTransformation))
            elif self.reset_zoom:
                frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                image = QImage(
                    frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(image))
                self.scale_factor = 1.0
                self.label.resize(self.label.pixmap().size())
                self.label.setPixmap(QPixmap.fromImage(image).scaled(
                    self.label.size(), QtCore.Qt.IgnoreAspectRatio,
                    QtCore.Qt.SmoothTransformation))
        except Exception as e:
            print(e)
            pass

    def open(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Select Image')
        if self.filename[0]:
            self.image = cv2.imread(str(self.filename[0]))
            frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image = QImage(
                frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(image))
            self.label.adjustSize()
            self.pathImageOpen.setText(self.filename[0])
            self.imageOpen = True

    def subtract_gradient(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Sélectionnez le fichier de gradient", "", "Images (*.jpg *.png *.bmp);;Tous les fichiers (*)", options=options)
        
        if file_name:
            gradient = cv2.imread(file_name)
            if gradient is not None:
                self.processed_image = cv2.subtract(self.image, gradient)
                frame = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(image))
                self.label.adjustSize()



    def method1(self):
        # Read the original image
        original_image = cv2.imread(self.filename[0], cv2.IMREAD_COLOR)

        # Calculate gradient
        gradient = cv2.Sobel(original_image, cv2.CV_64F, 1, 0, ksize=3)
        gradient = cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX)
        gradient = np.uint8(gradient)

        # Subtract gradient from the original image
        processed_image = cv2.subtract(original_image, gradient)

        # Display the processed image in the interface
        processed_frame = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        processed_image_display = QImage(processed_frame, processed_frame.shape[1], processed_frame.shape[0],
                                         processed_frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(processed_image_display))
        self.label.adjustSize()

    def method2(self):
        # Read the original image
        original_image = cv2.imread(self.filename[0], cv2.IMREAD_COLOR)

        # Convert the image to grayscale for processing
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        # Apply a threshold to detect pollution
        _, pollution_mask = cv2.threshold(
            gray_image, 200, 255, cv2.THRESH_BINARY)

        # Invert the mask to detect the region without pollution
        non_pollution_mask = cv2.bitwise_not(pollution_mask)

        # Darken the region without pollution
        original_image[non_pollution_mask >
                       0] = original_image[non_pollution_mask > 0] * 0.1

        # Display the processed image in the interface
        processed_frame = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        processed_image_display = QImage(processed_frame, processed_frame.shape[1], processed_frame.shape[0],
                                         processed_frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(processed_image_display))
        self.label.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Fenêtre()
    fenetre.show()
    sys.exit(app.exec_())
