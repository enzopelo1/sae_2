import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QPushButton, QButtonGroup, QGridLayout
from PyQt5.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

    #     # Création des radio boutons
    #     self.radio1 = QRadioButton("Radio 1", self)
    #     self.radio2 = QRadioButton("Radio 2", self)
    #     self.radio3 = QRadioButton("Radio 3", self)

    #     # Création du bouton poussoir
    #     self.pushButton = QPushButton("Appuyer", self)

    #     # Ajout des radio boutons à un groupe
    #     self.group = QButtonGroup(self)
    #     self.group.addButton(self.radio1)
    #     self.group.addButton(self.radio2)
    #     self.group.addButton(self.radio3)

    #     # Connexion du signal toggled()
    #     self.radio1.toggled.connect(self.on_radio1_toggled)

    #     # Disposition des widgets
    #     layout = QGridLayout(self)
    #     layout.addWidget(self.radio1, 0, 0)
    #     layout.addWidget(self.radio2, 1, 0)
    #     layout.addWidget(self.radio3, 2, 0)

    #     # Masquage du bouton poussoir
    #     self.pushButton.hide()

    #     # Ajout du bouton poussoir à droite
    #     layout.addWidget(self.pushButton, 3, 0, alignment=Qt.AlignRight)

    #     # Définir la largeur de la première colonne à 1
    #     layout.setColumnStretch(0, 1)

    #     self.setLayout(layout)

    # def on_radio1_toggled(self):
    #     # Si le premier bouton est sélectionné, le bouton poussoir apparaît
    #     if self.radio1.isChecked():
    #         self.pushButton.show()
    #     # Sinon, le bouton poussoir disparaît
    #     else:
    #         self.pushButton.hide()


    # Création des boutons radio
        self.radio1 = QRadioButton("Substract by gradient", self)
        self.radio2 = QRadioButton("Simple Threshold", self)

        self.pushButton = QPushButton("Import image...", self)

        self.group = QButtonGroup(self)
        self.group.addButton(self.radio1)
        self.group.addButton(self.radio2)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
