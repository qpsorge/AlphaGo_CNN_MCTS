from Goban import *

def copy_list(liste):
    
    # On se limite à 2 cas
    # if liste[0] == list:
    #     l1 = len(liste)
    #     l2 = len(liste[0])
    #     liste_copy = [[] for _ in range(l1)]
    #     for i in range(len(liste)):
    #         for j in range(len(liste[0])):
    #             liste_copy[i].append(liste[i][j])
    # else:
    #     liste_copy = [liste[i] for i in range(len(liste))]
    liste_copy = [liste[i] for i in range(len(liste))]
    return liste_copy
    

def copy_board(board):
    # On fait en sorte de travailler sur une copie du board et non sur le board directement:
    # Pour ça, on copie un à un tous les param:
    board_copy = Board()
    board_copy._nbWHITE = board._nbWHITE
    board_copy._nbBLACK = board._nbBLACK
    board_copy._capturedWHITE = board._capturedWHITE
    board_copy._capturedBLACK = board._capturedBLACK

    board_copy._nextPlayer = board._nextPlayer
    board_copy._board = copy_list(board._board)

    board_copy._lastPlayerHasPassed = board._lastPlayerHasPassed
    board_copy._gameOver = board._lastPlayerHasPassed

    board_copy._stringUnionFind = copy_list(board._stringUnionFind)
    board_copy._stringLiberties = copy_list(board._stringLiberties)
    board_copy._stringSizes = copy_list(board._stringSizes)

    board_copy._empties = board._empties

    board_copy._positionHashes = copy_list(board._positionHashes)
    board_copy._currentHash = board._currentHash
    board_copy._passHash = board._passHash 

    board_copy._seenHashes = board._seenHashes

    board_copy._historyMoveNames = copy_list(board._historyMoveNames)
    board_copy._trailMoves = copy_list(board._trailMoves)

    #Building fast structures for accessing neighborhood
    board_copy._neighbors = copy_list(board._neighbors)
    board_copy._neighborsEntries = copy_list(board._neighborsEntries)

    return board_copy


# Codage du rollout
# Complete one random playout from node
class Rollout:
    def __init__(self, node):
        self.node = node
        # On reprend la board du noeud à notre propre compte
        self._board = copy_board(node.board)


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
                self._board._nbWHITE += 1
                self._board._nextPlayer = self._board._BLACK
            else:
                self._board._nbBLACK += 1
                self._board._nextPlayer = self._board._WHITE
        else: #On a le cas d'un pass
            if self._board._lastPlayerHasPassed:
                self._board._gameOver = True
            else:
                self._board._gameOver = True



    def score(self):
        """
        On retourne 1 si victoire des noirs, 0.5 si égalité, 0 sinon
        réutilisation de result du GOBAN avec sortie différente
        """
        score = self._board._count_areas()
        score_black = self._board._nbBLACK + score[0]
        score_white = self._board._nbWHITE + score[1]
        if score_white > score_black:
            return 0
        elif score_white < score_black:
            return 1
        else:
            return 0.5

    # def move_possible(self, liste_moves):
    #     """
    #     On trie la posibilité des moves proposés
    #     """


    def lance_rollout(self):
    # On produit donc une partie aléatoire à partir du noeud
    # Implique: --> donner conditions de fin de partie
    # Boucler sous ces conditions l'avancement du board pour donner une note (victoire,defaite,égalité)
        while(not(self._board._gameOver)):
            # Choisir un move aléatoire parmis ceux légaux:
            liste_moves = self._board.generate_legal_moves()
            print("moves")
            print(liste_moves)
            # Est-ce qu'on s'assurerait pas que tous les moves sont possibles avant? --> Je pense que on est quand même bien for now
            alea = random.randint(0,len(liste_moves)-1)
            move = liste_moves[alea]
            self.play_move(move)
            print(self._board)

        # On récupère le resultat et attitre un score
        return self.score()

class Node:
    def __init__(self, board):
        self.board = board
        # On reprend la board du noeud à notre propre compte
        self.point = 0

# Test des rollout: On prend des boards de référence et on lance rollout:
'''
board = Board()
print(board)
print(board._board)
node = Node(board)
'''
# On test sur un board vide....
'''
roll = Rollout(node)
resultat = roll.lance_rollout()

'''

#print("let's check the board")
#print(roll._board)
# print("Le résultat est :" + str(resultat))
#print(board)
