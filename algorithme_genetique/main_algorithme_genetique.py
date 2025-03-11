import numpy as np

def fusion_poids_lognormal(l_parents, sigma, nb_fils = 4):
    """
    print(fusion_poids_lognormal(np.random.rand(1, 3),1))
    """

    l_fils = []
    for _ in range(nb_fils):
        poids = np.random.lognormal(1, sigma, len(l_parents))
        poids /= sum(poids)
        l_fils.append(np.average(l_parents, axis=0, weights=poids))

    return l_fils


def fusion_poids_normal(l_parents, sigma, nb_fils = 4):
    """
    print(fusion_poids_normal(np.random.rand(1, 3),1))
    """

    l_fils = []
    for _ in range(nb_fils):
        poids = np.random.normal(0, sigma, len(l_parents))
        poids /= sum(poids)
        l_fils.append(np.average(l_parents, axis=0, weights=poids))

    return l_fils


def bruitage(l_parents, sigma):
    """
    print(bruitage(np.random.rand(1, 3),.1))
    """

    l_fils = []
    for parent in l_parents:
        l_fils.append(parent + np.random.normal(0, sigma, len(parent)))
    
    return l_fils


def fusion_unif_hyper_sphere(l_parents, nb_fils = 4):
    """
    print(fusion_unif_hyper_sphere(np.random.rand(1, 3),1))
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
    l_v = np.random.rand(2,3)
    print(l_v)
    print(main_mutation(l_v, [0,2], 0.1 , 0.1))
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