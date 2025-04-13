Installation
==============

Voici les étapes pour installer et exécuter le logiciel.

1. Décompresser l'archive
-------------------------

Ouvre un terminal, place-toi dans le dossier contenant le fichier `.tar.gz` et tape :

.. code-block:: bash

   tar -xzf envisage-0.0.1.tar.gz


2. Aller dans le dossier du logiciel
------------------------------------

.. code-block:: bash

   cd envisage-0.0.1

3. Créer l'environnement Conda
------------------------------

.. code-block:: bash

   conda env create -f environment.yml

Sinon, lancer le script d'initialisation correspondant à votre système :

- **Pour Linux** :

  .. code-block:: bash

     ./linux_initialisation.sh

- **Pour macOS** :

  .. code-block:: bash

     ./mac_initialisation.zsh

- **Pour Windows** (via PowerShell) :

  .. code-block:: powershell

     ./windows_initialisation.ps1

4. Activer l’environnement
--------------------------

.. code-block:: bash

   conda activate env_isage

5. Lancer le logiciel
---------------------

.. code-block:: bash

   python src/main.py