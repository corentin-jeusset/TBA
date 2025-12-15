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
        self.history = []
        self.room_trail = []
    
    # Define the move method.
    def set_initial_room(self, room):
        """Définit la pièce de départ et l'ajoute à la pile de navigation."""
        self.current_room = room
        # Ajout de la pièce de départ à la pile de navigation (Room objects)
        self.room_trail.append(room)
    
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits.get(direction)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        old_room_description = self.current_room.description
        self.current_room = next_room
        self.room_trail.append(self.current_room)

        if old_room_description not in self.history:
             self.history.append(old_room_description)
             print(self.current_room.get_long_description())
        
        if self.history:
            print(self.get_history_string())

        return True
    
    def get_history_string(self):
        """
        Retourne la chaîne de caractères formatée représentant les pièces visitées.
        """
        
        if not self.history:
            return ""
        historique_joint = "\n""- ".join(self.history)
        return f"Vous êtes passés : \n- {historique_joint}\n"
    
    def back(self):
        """
        Déplace le joueur vers la pièce précédente en utilisant la pile de Rooms (self.room_trail).
        """
        # Il faut au moins deux éléments dans la pile pour pouvoir revenir en arrière,
        # car le premier élément est la pièce de départ.
        if len(self.room_trail) <= 1:
            print("\nVous êtes dans votre pièce de départ, vous ne pouvez pas revenir en arrière !\n")
            return False

        # 1. Retirer la pièce actuelle de la pile de navigation (objet Room)
        # L'objet Room de la pièce précédente est maintenant à l'indice [-1]
        self.room_trail.pop() 
        
        # 2. Récupérer la pièce précédente (objet Room)
        previous_room = self.room_trail[-1]
        
        # 3. Mettre à jour la pièce courante du joueur
        self.current_room = previous_room
        
        # 4. Maintien de la cohérence de l'historique d'affichage (descriptions)
        # On retire la description de la pièce que nous venons de 'dé-visiter'.
        if self.history:
             self.history.pop()
            
        # 5. Affichage du retour
        print(f"\nVous retournez à :\n{self.current_room.get_long_description()}")
        if self.history:
            print(self.get_history_string())
        else:
             print("Vous êtes revenu à votre point de départ.")
            
        return True