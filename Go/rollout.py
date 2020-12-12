from Goban import *

# Codage du rollout
# Complete one random playout from node
class Rollout:
    def __init__(self, node):
        self.node = node
        # On reprend la board du noeud à notre propre compte
        self._board = node.board   

    def play_move(self,move):
        # On a un plateau en entrée, maj de toutes les données
        color = self._board._nextPlayer
        # if self._board._nextPlayer == self.board._WHITE:
            # On check si le move est un suicide? --> pour les deux?
            # On maj nb de pièce --> voir si passe? avant
            # On insére le move dans le board
        if move != -1: #On passe le -1, la gestion du game over se fera après
            # On ajoute dans la bonne couleur du board
            self._board._put_stone(move,color)
            self._board._lastPlayerHasPassed = False
            if color == self._board._WHITE:
                self._board.nbWHITE += 1
                self._nextPlayer = self._board._BLACK
            else:
                self._board.nbBLACK += 1
                self._nextPlayer = self._board._WHITE

    def score(self):
        """
        On retourne 1 si victoire des blancs, 0.5 si égalité, 0 sinon
        réutilisation de result du GOBAN avec sortie différente
        """
        score = self._board._count_areas()
        score_black = self._board._nbBLACK + score[0]
        score_white = self._board._nbWHITE + score[1]
        if score_white > score_black:
            return 1
        elif score_white < score_black:
            return 0
        else:
            return 0.5

    # def move_possible(self, liste_moves):
    #     """
    #     On trie la posibilité des moves proposés
    #     """


    def lance_rollout(self,node):
    # On produit donc une partie aléatoire à partir du noeud
    # Implique: --> donner conditions de fin de partie
    # Boucler sous ces conditions l'avancement du board pour donner une note (victoire,defaite,égalité)
        while(not(self._board._gameOver)):
            # Choisir un move aléatoire parmis ceux légaux:
            liste_moves = self._board.legal_moves
            # Est-ce qu'on s'assurerait pas que tous les moves sont possibles avant? --> Je pense que on est quand même bien for now
            alea = random.randint(0,len(moves)-1)
            move = liste_moves[alea]S
            self.play_move(move)
        # On récupère le resultat et attitre un score
        return self.score()


# Test des rollout: On prend des boards de référence et on lance rollout:
