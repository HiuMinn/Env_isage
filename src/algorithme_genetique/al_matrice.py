import numpy as np
import torch


def fusion_poids_lognormal(l_parents, sigma, nb_fils=4):
    """
    :param l_parents: listes des individus choisis pour fusionner
    :type l_parents: array_like
    :param sigma: la variance de la log-normale pour distribuer les poids à des individus (les parents)
    :type sigma: float
    :param nb_fils: nombre de fils après la fusion. Défaut est 4 (nombre d'image à générer)
    :type nb_fils: int
    :return: listes des fils après la fusion
    :rtype: list[array_like]

    """


    if isinstance(l_parents, list):
        l_parents = torch.stack([p.squeeze(0) if p.dim() == 4 else p for p in l_parents])  # [n_parents, C, H, W]

    n_parents = l_parents.size(0)
    l_fils = []

    for _ in range(nb_fils):
        poids = torch.from_numpy(
            np.random.lognormal(mean=1, sigma=sigma, size=n_parents)
        ).float()
        poids /= poids.sum()

        poids = poids.view(-1, 1, 1, 1)  # pour [n_parents, C, H, W]
        enfant = torch.sum(l_parents * poids, dim=0)  # somme pondérée
        enfant = enfant.unsqueeze(0)
        l_fils.append(enfant)

    return l_fils


def fusion_poids_normal(l_parents, sigma, nb_fils=4):
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


    if isinstance(l_parents, list):
        l_parents = torch.stack(l_parents)  # [n_parents, C, H, W]

    n_parents = l_parents.size(0)
    l_fils = []

    for _ in range(nb_fils):
        poids = torch.from_numpy(
            np.random.ormal(mean=0, sigma=sigma, size=n_parents)
        ).float()
        poids /= poids.sum()

        poids = poids.view(-1, 1, 1, 1)  # pour [n_parents, C, H, W]
        enfant = torch.sum(l_parents * poids, dim=0)  # somme pondérée
        l_fils.append(enfant.unsqueeze(0))

    return l_fils

def bruitage(l_parents, sigma, reset_prob = 0.05):
    """
    Introduire la mutation sur chaque individu choisi avec une ditribution de loi normale

    :param l_parents: liste des individus choisis pour la mutation
    :type l_parents: array_like
    :param sigma: la variance de mutation suivi par la loi normale
    :type sigma: float
    :return: liste des individus mutés
    :rtype: list[array_like]

    """

    n_parents = len(l_parents)
    l_fils = []

    for parent in l_parents:
        # Mutation via distribution normale
        bruit = torch.normal(0, sigma, size=parent.shape)
        enfant_mutated = parent + bruit

        # Masque de réinitialisation aléatoire
        reset_mask = torch.rand_like(parent) < reset_prob
        enfant_mutated[reset_mask] = torch.randn_like(enfant_mutated[reset_mask])

        l_fils.append(enfant_mutated)

    return l_fils

def main_mutation(l_parents, schema, var_fusion=0, var_bruit=0, nb_fils=4):
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

    """
    l_courants = l_parents
    for num in schema:
        if num == 0:
            l_courants = fusion_poids_lognormal(l_courants, var_fusion, nb_fils)
        elif num == 1:
            l_courants = fusion_poids_normal(l_courants, var_fusion, nb_fils)
        elif num == 2:
            l_courants = bruitage(l_courants, var_bruit)
    return l_courants


# test via une visualisation de la distribution de 1000 fils à partir de 5 parents en 2D:

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # import doctest


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


    l_v = np.random.rand(5, 100,50)
    print(l_v)

    transforme_d1coup = main_mutation(l_v, [0, 2], 1, 0, nb_fils=1000)
    plot_evolution(l_v, transforme_d1coup, "transfo d'un coup")
    # doctest.testmod(optionflags=doctest.ELLIPSIS, verbose=True)