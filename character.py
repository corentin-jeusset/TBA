import random

class Character:
    def __init__(self, name, description, current_room, msgs):
        """
        Initialise un nouveau personnage non joueur (PNJ).

        :param name: Le nom du personnage (str)
        :param description: La description du personnage (str)
        :param current_room: Le lieu où se trouve le personnage (Room)
        :param msgs: Une liste de messages que le personnage peut dire (list)
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.weight = 0

    def __str__(self):
        """
        Retourne la représentation : Nom : description
        """
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """
        Affiche le prochain message du personnage et le place en fin de liste (rotation).
        """
        # Vérification de sécurité : si la liste est vide
        if not self.msgs:
            return "Ce personnage n'a rien à dire."

        # 1. On retire le premier message de la liste (le message actuel)
        message = self.msgs.pop(0)

        # 2. On le rajoute à la fin de la liste (pour la prochaine fois)
        self.msgs.append(message)

        # 3. On retourne le message pour qu'il soit affiché par le jeu
        return message
    
    def move(self):
        """
        Déplace le personnage aléatoirement vers une salle adjacente.
        Retourne True si le déplacement a eu lieu, False sinon.
        """
        from game import DEBUG
        
        # 1. Une chance sur deux de se déplacer
        # [True, False] simule le pile ou face
        if random.choice([True, False]):
            
            # Récupère les salles adjacentes (les valeurs du dictionnaire exits)
            # On convertit en liste pour utiliser random.choice
            possible_rooms = list(self.current_room.exits.values())

            # S'il n'y a pas de sortie, il ne peut pas bouger
            if not possible_rooms:
                return False

            # 2. Choisir une salle au hasard
            new_room = random.choice(possible_rooms)

            # Affichage de débogage
            if DEBUG:
                print(f"DEBUG: {self.name} se déplace de {self.current_room.name} vers {new_room.name}")
            
            # 3. Effectuer le déplacement (Mise à jour des dictionnaires)
            # A. On retire le personnage de la salle actuelle
            if self.name in self.current_room.characters:
                del self.current_room.characters[self.name]

            # B. On change la salle actuelle du personnage
            self.current_room = new_room

            # C. On ajoute le personnage dans la nouvelle salle
            new_room.characters[self.name] = self

            return True

        else:
            if DEBUG:
                print(f"DEBUG: {self.name} décide de rester dans {self.current_room.name}")
            return False