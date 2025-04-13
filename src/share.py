import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),"autoencodeur"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),"algorithme_genetique"))

from algorithme_genetique import al_matrice as ag

from autoencodeur import vae_plot as ae
import os
import random
import shutil

TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
ABS_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_LATENT = {}

def get_one_img():
    """
    récupère aléatoirement un image dans le fichier data
    :return:
    """
    file = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))
    #file = os.listdir("D:/Users/elisa/INFO7_BS/datasets/celeba_filtered")
    chosen_img = random.choice(file)
    return chosen_img

def add_to_tmp(img, j):
    """
    ajouter un image dans dossier temporaire tmp
    """
    source = os.path.join(ABS_DIR,f"data/{img}")
    #source = f"D:/Users/elisa/INFO7_BS/datasets/celeba_filtered/{img}"

    name = f"img{j+1}"

    destination = os.path.join(TMP_DIR,f"{name}.jpg")
    shutil.copy(source, destination)
    return os.path.join(TMP_DIR,f"{name}.jpg") #name

def clear_tmp():
    """
    Vider les images dans tmp
    :return: None
    """
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"tmp")
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        os.remove(file_path)

def already_chosen_img(img, chosen_img_set):
    """
    vérifier si l'image a été choisi
    :param img: l'image à vérifier
    :param chosen_img_set: l'ensemble des images choisis
    :type return: bool
    """
    if img in chosen_img_set : 
        return True 
    else : 
        chosen_img_set.add(img)
        return False 
    
def add_to_dict(key, value):
    """
    Mettre a jour le dictionnaire dans un fichier
    :param key: le répertoire absolu du fichier image
    :param value: vecteur latent encodée de l'image correspondant
    :return:
    """
    DICT_LATENT[key] = value

def replace_20_first_img_in_directory(nb=20):
    """
    mets 20 img avec les bons noms : les indexes 1,2,...,21 dans le dossier
    :param nb: nombre d'image initiale
    """
    #clear_tmp()
    chosen_img_set = set()
    for j in range(nb):
        img = get_one_img()

        while already_chosen_img(img, chosen_img_set):
            img = get_one_img()

        i = add_to_tmp(img, j)
        add_to_dict(i,ae.encode(i))


def generate_img(l_of_one_img_name, var=0.2):
    """
    Varier l'image sélectionné pour la mutation
    :param l_of_one_img_name: list de répertoire de l'image à générer
    :param var: Variance du bruit appliquer sur l'image
    :return: None
    """
    parent = [DICT_LATENT[l_of_one_img_name[0]]]
    l_vec_son = ag.bruitage([val for val in parent for _ in range(4)], sigma = var) #appliquer la mutation a 4 enfants d'image choisi
    start = len(DICT_LATENT)
    for i,vec in enumerate(l_vec_son):
        img = ae.decode(vec)
        file_name = os.path.join(TMP_DIR, f"img{start+i+1}.jpg")
        ae.save_image( img,file_name,path="")
        add_to_dict(file_name,vec)

def combine_img(l_of_img_names,var_bruit = 0.25,var_fusion= 0.65):
    """
    Combiner les images sélectionner en utilisant algorithme génétique
    :param l_of_img_names: list des répertoires des images sélectionnées
    :param var_fusion: variance des poids tirés par les lois définis
    :return: None
    """
    l_vec_parents = [DICT_LATENT[name] for name in l_of_img_names]
    l_vec_son = ag.main_mutation(l_vec_parents, schema=[0,2],var_bruit=var_bruit,var_fusion=var_fusion,nb_fils=4)
    start = len(DICT_LATENT)
    for i,vec in enumerate(l_vec_son):
        img = ae.decode(vec)
        file_name = file_name = os.path.join(TMP_DIR, f"img{start+i+1}.jpg")
        ae.save_image(img,file_name,path="")
        add_to_dict(file_name,vec)


