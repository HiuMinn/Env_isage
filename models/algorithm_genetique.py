import numpy as np
import random

class GA():
    def __init__(self,nb_individu,nb_generations):
        """
        Initialiser les parametres de la classe GA
        Args:
            nb_individu (int): nombre d'individu
            nb_generations (int): nombre de generations pour l'evolution genetique
        """
        #initialiser les parametres des
        self.nb_individu=nb_individu
        self.nb_generations=nb_generations
        #parametres de populations
        self.fitness = [] #TODO : definition de fitness
        self.population = []

    def add_individual(self,individual):
        """
        Ajouter un individu a la population
        param
            individual (object):
        return:
        """
        #TODO : definir individual (images,veteurs)
        self.population.append(individual)
        self.fitness.append(individual.fitness)

    def selection(self):
        """
        selectionner une sous-population a reproduire pour la prochaine generation
        return:
            selected (list): les individus a reproduire
        """
        #TODO
        selected = []
        return selected

    def crossover(self, parent1, parent2):
        """
        Appliquer le technique de croisement pour generer de nouvelles descendant
        param
            parent1 (object):
            parent2 (object):
        return:
        """
        #TODO
        return
