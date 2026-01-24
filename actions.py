# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False
"""
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        exits = player.current_room.exits
        # 1. Récupérer la direction saisie par le joueur
        direction = list_of_words[1]

        if direction in exits:
            player.move(direction)
            
            # --- VÉRIFICATION DU GAME OVER SEULEMENT ---
            if getattr(player.current_room, 'is_deadly', False):
                print("\n=== GAME OVER ===")
                game.finished = True
            if player.current_room.name == "Plain":
                print("\n🎉 FÉLICITATIONS ! Vous avez atteint la fin de l'aventure. 🎉")
                
                # Petit bonus pour voir tes récompenses à la fin :
                player.show_rewards()
                
                game.finished = True
                return True
                
            return True
        
        # 3. Si la direction n'existe pas
        print("\nCette direction n'existe pas.")
        return False

        # normalisation simple d'une candidate direction
        def normalize(s):
            m = {
                "n": "N", "NORD": "N", "Nord": "N", "nord": "N",
                "e": "E", "EST": "E", "Est": "E", "est": "E",
                "s": "S", "SUD": "S", "Sud": "S", "sud": "S",
                "o": "O", "OUEST": "O", "Ouest": "O", "ouest": "O"
            }
            return m.get(s.strip().lower(), s.strip().upper())

        # candidate initiale si fournie (ex: 'go N')
        candidate = list_of_words[1]

        while True:
            # si on n'a pas de candidate, lire une ligne et la traiter
            if candidate is None:
                line = input("> ").strip()
                if not line:
                    continue
                parts = line.split()
                # si l'entrée est 'go <dir>' on prend la direction comme candidate
                if parts[0].lower() == "go" and len(parts) > 1:
                    candidate = parts[1]
                else:
                    # sinon traiter la ligne comme une commande normale
                    game.process_command(line)
                    if getattr(game, "finished", False):
                        return False
                    # après exécution, on redemande (candidate reste None)
                    continue

            # tenter la candidate
            direction = normalize(candidate)
            next_room = exits.get(direction)
            if next_room is not None:
                player.move(direction)
                return True

            # candidate invalide : message + ré-affichage des sorties, puis redemande
            print("\nCette direction n'existe pas. Veuillez en choisir une autre.")
            print(player.current_room.get_long_description())
            candidate = None

            current_room = game.player.current_room

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    def back(game, list_of_words, number_of_parameters) :
        game.player.back()
        return False
    
    def look(game, list_of_words, number_of_parameters): # Ajoutez bien ces 3 paramètres
        """
        Affiche les objets présents dans la pièce actuelle.
        """
        # 1. Vérification des paramètres (look ne prend pas d'argument après le mot "look")
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            # On utilise MSG0 car look se tape seul
            print(f"\nLa commande '{command_word}' ne prend pas de paramètre.\n")
            return False
        
        # 2. Logique de la commande
        room = game.player.current_room
        
        # Affiche la description de base (le lieu et les sorties)
        print(room.get_long_description())

        # Vérifie si la salle est vraiment vide (ni objets, ni persos)
        if not room.inventory and not room.characters:
            print("Il n'y a rien d'autre ici.")
            return True

        print("On voit :")
        
        # 1. Boucle pour les objets (Item)
        for item in room.inventory.values():
            print(f"    - {item.name} : {item.description} ({item.weight} kg)")
            
        # 2. Boucle pour les personnages (Character)
        for character in room.characters.values():
            print(f"    - {character.name} : {character.description}")
            
        return True
    
    def inventory(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(f"\nLa commande '{list_of_words[0]}' ne prend pas de paramètre.\n")
            return False
        print(game.player.get_inventory())
        return True
    
    # Dans actions.py

    def take(game, list_of_words, number_of_parameters):
        # 1. VÉRIFICATION DES PARAMÈTRES (MODIFIÉE pour accepter plusieurs mots)
        if len(list_of_words) < 2:
            print(f"\nLa commande '{list_of_words[0]}' prend au moins 1 paramètre.\n")
            return False
        
        # FUSION DES MOTS : "Bouteille", "de", "Rhum" devient "Bouteille de Rhum"
        target_name = " ".join(list_of_words[1:])
        
        player = game.player
        current_room = player.current_room
        
        # -------------------------------------------------------------
        # CAS 1 : C'EST UN OBJET (ITEM)
        # -------------------------------------------------------------
        if target_name in current_room.inventory:
            item = current_room.inventory[target_name]
            current_weight = player.get_current_weight()

            # Vérification du poids
            if current_weight + item.weight > player.max_weight:
                print(f"\n[ERREUR] Cet objet est trop lourd !")
                print(f"Poids de l'objet : {item.weight} kg")
                print(f"Capacité restante : {player.max_weight - current_weight} kg\n")
                return False
            # Transfert de l'objet
            player.inventory[target_name] = current_room.inventory.pop(target_name)
            print(f"\nVous avez pris : {target_name}.\n")

            # --- LES DEUX LIGNES À AJOUTER ICI ---
            player.quest_manager.complete_objective("Récupérer la bouteille de Rhum")
            return True

        # -------------------------------------------------------------
        # CAS 2 : C'EST UN PERSONNAGE (CHARACTER)
        # -------------------------------------------------------------
        elif target_name in current_room.characters:
            npc = current_room.characters[target_name]
        
            # On définit quels personnages sont "prenables" (ex: Chien, Chat)
            # Vous pouvez modifier cette liste selon vos besoins
            compagnons_possibles = ["Fletcher"]

            if npc.name in compagnons_possibles:
                # On vérifie le poids aussi pour le personnage !
                # Note : Assurez-vous que la classe Character possède un attribut self.weight
                current_weight = player.get_current_weight()
            
                # Si le Character n'a pas de poids défini, on considère 0 par défaut (sécurité)
                npc_weight = getattr(npc, "weight", 0) 

                if current_weight + npc_weight > player.max_weight:
                    print(f"\n[ERREUR] {npc.name} est trop lourd pour être porté/guidé !")
                    return False

                # Transfert du personnage vers l'inventaire du joueur
                player.inventory[target_name] = current_room.characters.pop(target_name)
                print(f"\n{target_name} est maintenant votre compagnon et vous suit partout !\n")
                return True
            else:
                print(f"\n{target_name} refuse de vous suivre.\n")
                return False

        # -------------------------------------------------------------
        # CAS 3 : RIEN TROUVÉ
        # -------------------------------------------------------------
        else:
            print(f"\nIl n'y a pas de '{target_name}' ici.\n")
            return False
        

    def drop(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de déposer un objet au sol.
        Usage : drop <nom_objet>
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(f"\nLa commande '{list_of_words[0]}' prend 1 paramètre (le nom de l'objet).\n")
            return False

        item_name = list_of_words[1]
        player = game.player

        # Vérifier si le joueur possède l'objet
        if item_name in player.inventory:
            # Retirer du joueur et mettre dans la pièce
            item = player.inventory.pop(item_name)
            player.current_room.inventory[item_name] = item
            print(f"\nVous avez déposé : {item_name}.\n")
            return True
    
        print(f"\nVous n'avez pas de '{item_name}' dans votre inventaire.\n")
        return False
    
    def check(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur.
        Cette commande ne prend pas de paramètre.
        """
        # 1. Vérification du nombre de paramètres (doit être 1 : juste "check")
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            # On utilise MSG0 car check se tape seul
            print(f"\nLa commande '{command_word}' ne prend pas de paramètre.\n")
            return False
        
        # 2. Appel de la méthode get_inventory du joueur et affichage
        # Rappel : game.player.get_inventory() retourne la chaîne formatée
        print(game.player.get_inventory())
        return True
    
    def talk(game, list_of_words, number_of_parameters):
        """
        Permet de discuter avec un personnage présent dans la pièce OU dans l'inventaire.
        Commande : talk <nom_du_personnage>
        """
        # On vérifie d'abord si la liste contient bien au moins 2 mots (talk + nom)
        if len(list_of_words) < 2:
            print("\nAvec qui voulez-vous parler ? (Exemple: 'talk <nom>')\n")
            return False

        # Maintenant on peut lire l'index [1] sans risque de crash
        npc_name = list_of_words[1]
        current_room = game.player.current_room

        # On vérifie si le personnage est présent dans la pièce
        if npc_name in current_room.characters:
            character = current_room.characters[npc_name]
            # On appelle la méthode pour obtenir un message aléatoire ou défini
            print(f"\n{character.name} : {character.get_msg()}")
            return True
        else:
            print(f"\nIl n'y a pas de '{npc_name}' ici.")
            return False

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True

    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True

    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True
        
        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)

        return False
    
    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        # Show all rewards
        game.player.show_rewards()
        return True