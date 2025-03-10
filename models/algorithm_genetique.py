import numpy as np
import random

class GA():
    def __init__(self,x,nb_individu=100):
        """
        Initialiser les parametres de la classe GA
        Arg:
            x (list des arrays): l'ensemble des vecteurs de photos
            nb_individu (int): le nombre d'individu dans une population
        """
        #initialiser les parametres des
        self.input = x
        self.nb_individu=nb_individu
        #parametres de populations
        self.fitness = [] #TODO : definition de fitness
        self.population = []
        self.init_population()

    def init_population(self):
        """
        initialiser la première population
        :return: None
        """
        for i in range(self.nb_individu):
            self.population.append([]) #TODO: Définir l'individu
        return

    def tournament_selection(self,tournament_size):
        """
        selectionner une sous-population a reproduire pour la prochaine generation selon tournament
        argument:
            tournament_size (int): nombre d'individu a utiliser pour le tournament
        return:
            selected (list): les individus a reproduire
        """
        #TODO
        selected = []
        for _ in range(len(self.population)):
            tournament = random.sample(list(zip(self.population,self.fitness)), tournament_size)
            winner = max(tournament, key=lambda x: x[1])
            selected.append(winner)
        return selected

    def crossover(self, parent1, parent2):
        """
        Appliquer le technique de croisement pour generer de nouvelles descendant
        Args:
            parent1, parent2 (object):
        return:
        """
        #TODO
        return

    def genetic_algorithm(self,nb_generations):
        """
        Générer les nouvelles populations
        Args:
            nb_generations (int): nombre de generations pour l'évolution genetique

        return: les images les plus pertinentes (meilleurs fitness)
        """
        res = []
        for i in range(nb_generations):
            sous_population = self.tournament_selection(5)

        return