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
    for _ in range(nb):
        img = get_one_img()
        i = add_to_tmp(img)
        add_to_dict(i,encode(img))


def generate_img(l_of_one_img_name, var):
    l_vec_son = ag.bruitage([dict_encoded[l_of_one_img_name[0]]], sigma = var) # remplacé par main_mutation si besoin
    for vec in l_vec_son:
        img = ae.decode(vec)
        i = add_to_tmp(img)
        add_to_dict(i,vec)



def combine_img(l_of_img_names,var):
    img_vec_dict = read_dict()
    l_vec_parents = [img_vec_dict[name] for name in l_of_img_names]
    l_vec_son = ag.fusion_poids_lognormal(l_vec_parents, var)

    for vec in l_vec_son:
        img = ae.decode(vec)
        i = add_to_tmp(img)
        add_to_dict(i,vec)


if __name__=='__main__':
    app = ig.QApplication(sys.argv)
    window = ig.WelcomeScreen()
    window.show()
    sys.exit(app.exec())
    with open(FILENAME, "w") as f: #vider le fichier
        pass