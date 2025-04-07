import sys
sys.path.append("./interface_graphique/")
sys.path.append("./autoencodeur/")
sys.path.append("./algorithme_genetique/")

import numpy as np
from PIL import Image

from algorithme_genetique import main_algorithme_genetique as ag
#from interface_graphique import test7 as ig
from autoencodeur import vae_plot as ae
import json

import os
import random
import shutil

FILENAME = "src/tmp/dict_vect.txt"

def get_one_img():
    file = os.listdir("src/data")
    #file = os.listdir("D:/Users/elisa/INFO7_BS/datasets/celeba_filtered")
    chosen_img = random.choice(file)
    return chosen_img

def add_to_tmp(img, j):
    source = f"src/data/{img}"
    #source = f"D:/Users/elisa/INFO7_BS/datasets/celeba_filtered/{img}"
    if j < 10 : 
        name = f"00{j}"
        
    else : 
        name = f"0{j}"
    destination = f"src/tmp/{name}.png"
    shutil.copy(source, destination)
    return f"{name}.png" #name

def clear_tmp():
    folder = "src/tmp"
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        os.remove(file_path) 

def already_chosen_img(img, chosen_img_set): 
    if img in chosen_img_set : 
        return True 
    else : 
        chosen_img_set.add(img)
        return False 
    
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
    chosen_img_set = set()
    for j in range(nb):
        img = get_one_img()

        while already_chosen_img(img, chosen_img_set):
            img = get_one_img()

        i = add_to_tmp(img, j)
        add_to_dict(i,ae.encode(img)) 


def generate_img(l_of_one_img_name, var):
    img_vec_dict = read_dict()
    l_vec_son = ag.bruitage([img_vec_dict[l_of_one_img_name[0]]], sigma = var) # remplacé par main_mutation si besoin
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
    """app = ig.QApplication(sys.argv)
    window = ig.WelcomeScreen()
    window.show()
    sys.exit(app.exec())
    with open(FILENAME, "w") as f: #vider le fichier
        pass"""
    replace_20_first_img_in_directory()