# Define the Player class.
class Player():
    """
    Classe représentant un joueur dans le jeu.

    Le joueur possède un nom et se déplace de pièce en pièce en fonction des sorties disponibles.

    Attributs :
        name (str) : nom du joueur.
        current_room (Room) : pièce où se trouve actuellement le joueur.

    Méthodes :
        move(direction) : déplace le joueur dans la direction donnée si une sortie existe.

    Exceptions :
        KeyError : levée si la direction n'existe pas dans les sorties de la pièce courante.

    Exemples :
    >>> p = Player("Théo")
    >>> p.current_room = room1 
    >>> p.move("nord")
    True
    >>> p.move("sud")
    Aucune porte dans cette direction !
    False
    """

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    