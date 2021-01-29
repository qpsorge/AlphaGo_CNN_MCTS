# Approche de création d'un joueur de go en s'inspirant d'AlphaGo et MonteCarloTreeSearch

Projet réalisé par Gwenaelle Cadic et Quentin Pestre-Sorge

### Externals requirements
* Gnugo

## Work done :
* Data preprocessing of boards (separation in binaries feature maps => Shape : (9,9,2) )
* Data augmentation of boards  (rotations)
* CNN model training and saved : cnn_model4prior.h5
* Coding of MCTS (Tree & Nodes) 
* Coding of Rollout
## Possible improvements :
* Data augmentation (symmetry)
* Link MCTS to let the player be playable (link our MCTS decision making to myPlayer.py getPlayerMove)


## Stratégie
Basée sur alphaGo, notre objectif était de réaliser un joueur de Go capable de rivaliser/vaincre un autre joueur lambda débutant.
La stratégie de ce joueur était d'exploiter principalement 3 éléments :
* Un réseau de neurone convolutionnel entrainé permettant d'évaluer l'état du jeu et donnant une estimation du pourcentage de victoire de chaque joueur.
* Un MonteCarloTreeSearch, permettant d'affiner le choix du move à jouer pour le joueur
* Un rollout, qui permettrait d'aider le MCTS à affiner son choix en simulant des parties aléatoires

L'idée était de réaliser plusieurs opérations sur le MCTSTree, en boucle durant un certains temps :
* Expand (expand possible childs : creation of nodes and initialisation of their priors with CNN)
* Rollout on the node that was expanded
* Backpropagation to update visits and values of parents nodes
Ce qui permettait d'obtenir une estimation des meilleurs coups à jouer.
Après quoi, le joueur de go connaitrait les meilleurs coups à jouer.
Il aurait alors pu choisir le meilleurs coups parmis les coups légaux.

### CNN : Alpha_GO_CNN_model.ipynb, cnn_model4prior.h5
L'idée des noyaux de taille (5,5) vient de papiers implémentant alphaGo ayant de bons résultats.

Notre modèle est from scratch : 1 742 865 paramètres.

Soit Mod((n,n), f) un module constitué d'une convolution2D (f filtres convolutionnels avec noyaux de taille (n,n)) suivie d'une Batch Normalisation, fonction d'activation ReLU et same padding.
##### Extraction de features
* 1 x Mod((5,5), 128) 
* 4 x Mod((5,5), 64) 
* 2 x Mod((3,3), 32)
* 1 x Mod((3,3), 16)
* Flatten
##### Exploitation des features extraites
* 3 x Dense(512, relu)
* Dropout à 50%
* Dense(1, sigmoid) 

=> probability between 0 and 1 as an output


### Génie Logiciel
Classes has been implemented to design the rollout, the MCTS tree & the MCTS nodes :
* Rollout (in rollout.py)
* MCTSNode (in MCTS.py)
* MCTSTree (in MCTS.py)

##### The Goban was provided by Laurent Simon