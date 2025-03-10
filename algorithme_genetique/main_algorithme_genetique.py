import numpy as np

def fusion_poids_lognormal(l_parents, sigma, nb_fils = 4):
    """
    print(fusion_poids_lognormal(np.random.rand(1, 3),1,1))
    """

    l_fils = []
    for _ in range(nb_fils):
        poids = np.random.lognormal(1, sigma, len(l_parents))
        poids /= sum(poids)
        l_fils.append(np.average(l_parents, axis=0, weights=poids))

    return l_fils


def fusion_poids_normal(l_parents, sigma, nb_fils = 4):
    """
    print(fusion_poids_normal(np.random.rand(1, 3),1,1))
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


def main_mutation(l_parents, schema, var_poids, var_bruit):
    """
    l_v = np.random.rand(2,3)
    print(l_v)
    print(main_mutation(l_v, [0,2], 0.1 , 0.1))
    """
    l_courants = l_parents
    for num in schema:
        if num == 0:
            l_courants = fusion_poids_lognormal(l_courants, var_poids)
        elif num == 1:
            l_courants = fusion_poids_normal(l_courants, var_poids)
        elif num == 2:
            l_courants = bruitage(l_courants, var_bruit)
    return l_courants