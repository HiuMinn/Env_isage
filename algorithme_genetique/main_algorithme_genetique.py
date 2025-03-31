import numpy as np

def fusion_poids_lognormal(l_parents, sigma, nb_fils = 4):
    """
    :param l_parents: listes des individus choisis pour fusionner
    :type l_parents: array_like
    :param sigma: la variance de la log-normale pour distribuer les poids à des individus (les parents)
    :type sigma: float
    :param nb_fils: nombre de fils après la fusion. Défaut est 4 (nombre d'image à générer)
    :type nb_fils: int
    :return: listes des fils après la fusion
    :rtype: list[array_like]

    :Example:

    >>> fusion_poids_lognormal(np.array([[0.37457261, 0.39321517, 0.49215443],[0.42096036, 0.51902773, 0.36207469]]),0)
    [array([0.39776649, 0.45612145, 0.42711456]), array([0.39776649, 0.45612145, 0.42711456]), array([0.39776649, 0.45612145, 0.42711456]), array([0.39776649, 0.45612145, 0.42711456])]


    """
    l_fils = []
    for _ in range(nb_fils):
        poids = np.random.lognormal(1, sigma, len(l_parents))
        poids /= sum(poids)
        l_fils.append(np.average(l_parents, axis=0, weights=poids))

    return l_fils


def fusion_poids_normal(l_parents, sigma, nb_fils = 4):
    """
    Fusionner les individus avec des poids tirés suivi par la loi normale

    :param l_parents: listes des individus choisis pour fusionner
    :type l_parents: array_like
    :param sigma: sigma des poids suivi par la loi normale
    :type sigma: float
    :param nb_fils: nombre de fils après la fusion. Défaut est 4 (nombre d'image à générer)
    :type nb_fils: int
    :return: listes des fils après la fusion
    :rtype: list[array_like]

    :Example:

    fusion_poids_normal(np.random.rand(2,3),1)
    """

    l_fils = []
    for _ in range(nb_fils):
        poids = np.random.normal(0, sigma, len(l_parents))
        poids /= sum(poids)
        l_fils.append(np.average(l_parents, axis=0, weights=poids))

    return l_fils


def bruitage(l_parents, sigma):
    """
    Introduire la mutation sur chaque individu choisi avec une ditribution de loi normale

    :param l_parents: liste des individus choisis pour la mutation
    :type l_parents: array_like
    :param sigma: la variance de mutation suivi par la loi normale
    :type sigma: float
    :return: liste des individus mutés
    :rtype: list[array_like]

    :Example:
    >>> bruitage(np.array([[0.7469792 , 0.98221673, 0.533432  ],[0.19599989, 0.04993301, 0.17879477]]),0)
    [array([0.7469792 , 0.98221673, 0.533432  ]), array([0.19599989, 0.04993301, 0.17879477])]
    """

    l_fils = []
    for parent in l_parents:
        l_fils.append(parent + np.random.normal(0, sigma, len(parent)))
    
    return l_fils


def fusion_unif_hyper_sphere(l_parents, nb_fils = 4):
    """
    Fusionner les individus avec des poids tirés aléatoirement pour générer un hyper-sphere

    :param l_parents: listes des individus choisis pour fusionner
    :type l_parents: list
    :param nb_fils: nombre de fils après la fusion. Défaut est 4 (nombre d'image à générer)
    :type nb_fils: int
    :return: listes des fils après la fusion
    :rtype: list[array_like]

    :Example:

    fusion_unif_hyper_sphere(np.random.rand(2,3),1)

    """
    centre = np.mean(l_parents, axis=0)
    rayon = np.max([parent - centre for parent in l_parents])
    l_fils = []
    for _ in range(nb_fils):
        direction = np.random.uniform(low=-1, high=1, size=len(centre))
        print("dir",direction)
        l_fils.append(np.random.uniform(-1,1) * rayon * direction/np.linalg.norm(direction)+centre)

    return l_fils


def main_mutation(l_parents, schema, var_fusion = 0, var_bruit = 0, nb_fils=4):
    """
    Pipeline pour fusionner et faire la mutation sur l'ensemble des individus choisis

    :param l_parents: listes des individus choisis pour la mutation
    :type l_parents: array_like
    :param schema: l'étape de la fusion et de la mutation
    :type schema: list[int]
    :param var_fusion: variance de la fusion
    :type var_fusion: float
    :param var_bruit: variance de la mutation
    :type var_bruit: float
    :param nb_fils: nombre de fils après la fusion et la mutation. Défaut est 4 (nombre d'image à générer)
    :type nb_fils: int
    ...
    :return: listes des individus fusionnés et mutés
    :rtype: list[array_like]

    :Example:

    >>> main_mutation(np.array([[0.37457261, 0.39321517, 0.49215443],[0.42096036, 0.51902773, 0.36207469]]), [0,2], 0 , 0)
    [array([0.39776649, 0.45612145, 0.42711456]), array([0.39776649, 0.45612145, 0.42711456]), array([0.39776649, 0.45612145, 0.42711456]), array([0.39776649, 0.45612145, 0.42711456])]

    """
    l_courants = l_parents
    for num in schema:
        if num == 0:
            l_courants = fusion_poids_lognormal(l_courants, var_fusion, nb_fils)
        elif num == 1:
            l_courants = fusion_poids_normal(l_courants, var_fusion, nb_fils)
        elif num == 2:
            l_courants = bruitage(l_courants, var_bruit)
        elif num == 3:
            l_courants = fusion_unif_hyper_sphere(l_courants, nb_fils)
    return l_courants


# test via une visualisation de la distribution de 1000 fils à partir de 5 parents en 2D:

if __name__== '__main__':

    import matplotlib.pyplot as plt
    import doctest
    def plot_evolution(initial, transforme, titre):
        plt.figure(figsize=(8, 6))
        plt.scatter(initial[:, 0], initial[:, 1], color='blue', label='parents')
        transforme = np.array(transforme)
        plt.scatter(transforme[:, 0], transforme[:, 1], color='red', label='fils')
        plt.legend()
        plt.title(titre)
        plt.xlabel("Dimension 1")
        plt.ylabel("Dimension 2")
        plt.show()

    l_v = np.random.rand(5, 2)
    print(l_v)

    transforme_d1coup = main_mutation(l_v, [0,2], 1, 0, nb_fils=1000)
    plot_evolution(l_v,transforme_d1coup, "transfo d'un coup")
    doctest.testmod(optionflags=doctest.ELLIPSIS,verbose=True)