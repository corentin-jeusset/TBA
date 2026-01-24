# Define the Player class.

from quest import QuestManager

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
        self.inventory = {}
        self.max_weight = 10
        self.move_count = 0
        self.rewards = [] # List to store earned rewards
        self.quest_manager = QuestManager(self)  

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

        self.quest_manager.check_room_objectives(self.current_room.name)

        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

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
    
    def get_inventory(self):
        if not self.inventory:
            return "Votre inventaire est vide."
        
        items_str = "\n".join([f"  - {item}" for item in self.inventory.values()])
        return f"Vous portez actuellement :\n{items_str}"

    def get_inventory(self):
        if not self.inventory:
            return f"Votre inventaire est vide. (Charge : 0/{self.max_weight} kg)"
    
        items_str = "\n".join([f"    - {item}" for item in self.inventory.values()])
        current_w = self.get_current_weight()
    
        return (f"Vous disposez des items suivants :\n{items_str}\n"
                f"Poids total : {current_w}/{self.max_weight} kg")
    
    def get_current_weight(self):
        """Calcule le poids total des objets dans l'inventaire."""
        total_weight = 0
        for item in self.inventory.values():
            total_weight += item.weight
        return total_weight
    
    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")

    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()