# Define the Room class.

class Room:

    """
    Cette classe permet de représenter une pièce.

    Elle modélise une salle contenant un nom, une description,
    ainsi que des sorties permettant de se déplacer vers d'autres pièces.

    Attributs :
        name (str) : Le nom de la pièce.
        description (str) : La description de la pièce.
        exits (dict[str, Room]) : Un dictionnaire associant une direction (str) à une autre instance de Room représentant la sortie correspondante.

    Méthodes :
        __init__(self, name, description) : Le constructeur.
        get_exit(self, direction) : Retourne la salle correspondant à la direction indiquée ou None si aucune sortie ne correspond.
        get_exit_string(self) : Retourne une chaîne décrivant l’ensemble des sorties disponibles.
        get_long_description(self) : Retourne une description complète de la pièce incluant la liste des sorties.
    
    Exemples :
    >>> hall = Room("Hall", "dans le hall d'entrée")
    >>> cuisine = Room("Cuisine", "dans la cuisine")
    >>> hall.exits["nord"] = cuisine
    >>> hall.get_exit("nord") is cuisine
    True
    >>> hall.get_exit("sud") is None
    True
    >>> "nord" in hall.get_exit_string()
    True
    >>> "Sorties:" in hall.get_long_description()
    True

    """

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
