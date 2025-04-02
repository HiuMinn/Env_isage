import sys
sys.path.append("./interface_graphique/")
sys.path.append("./autoencodeur/")
sys.path.append("./algorithme_genetique/")
import numpy as np
from PIL import Image
import algorithme_genetique as ag
import interface_graphique as ig
import torch
import autoencodeur as ae

def get_one_img()

def clear_tmp():
    pass

def add_to_tmp(img):
    pass


def clear_tmp():
    pass

def add_to_dict(key, value):
    pass


def replace_20_first_img_in_directory(nb=20):
    """
    mets 20 img avec les bons noms : les indexes 1,2,...,21 dans le dossier
    """
    clear_tmp()
    for i in range(nb):
        img = get_one_img()
        add_to_tmp(img)
        add_dict
        
    return dict_encoded


def generate_img(l_of_one_img_name, var):
    """
    input : liste d'un seul nom d'image
    rajoute les 4 images générées au dossier
    """
    l_vectors = ag.bruitage([dict_encoded[l_of_one_img_name[0]]], sigma = var)
    for vec in l_vectors:
        img = ae.decode(vec)
        add_to_tmp(img)

    return dict_encoded


def combine_img(l_of_img_names):
    """
    input : liste de plusieurs noms d'images
    rajoute les 4 images générées au dossier
    """
    return dict_encoded


if __name__=='__main__':
    app = ig.QApplication(sys.argv)
    window = ig.WelcomeScreen()
    window.show()
    sys.exit(app.exec())
