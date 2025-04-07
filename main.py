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
import json

FILENAME = "./tmp/dict_vect.txt"
def get_one_img():
    pass
def clear_tmp():
    pass

def add_to_tmp(img):
    pass


def clear_tmp():
    pass

def add_to_dict(key, value):
    """
    Mettre a jour le dictionnaire dans le fichier
    :param key:
    :param value:
    :return:
    """
    with open(FILENAME, "a") as fichier:
        fichier.write(f"{key}:{json.dumps(value.tolist() if isinstance(value, np.ndarray) else value)}\n")

def read_dict():
    data = {}
    try:
        with open(FILENAME,"r") as f:
            for line in f:
                key,value = line.strip().split(":")
                parsed_value = json.loads(value)  # Convertit JSON en liste/array
                data[int(key)] = np.array(parsed_value) if isinstance(parsed_value, list) else parsed_value

    except FileNotFoundError:
        pass # si le fichier n'existe pas encore
    return data


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
    with open(FILENAME, "w") as f: #vider le fichier
        pass