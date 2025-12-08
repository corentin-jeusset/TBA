# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        
        # Setup rooms

        crossing = Room("Crossing", "à un croisement de plusieurs chemin, dans une étendue verte.")
        self.rooms.append(crossing)
        meadow = Room("Meadow", "dans une prairie, un vent frais vous caresse.")
        self.rooms.append(meadow)
        forest = Room("Forest", "dans une forêt, un brouillard gêne votre visibilité.")
        self.rooms.append(forest)
        marshes = Room("Marshes", "dans des marécages, une odeur nauséabonde en émane.")
        self.rooms.append(marshes)
        lake = Room("Lake", "au bord d'un lac, le brouillard s'est intensifié.")
        self.rooms.append(lake)
        fishing_boat = Room("Fishing boat", "à coté d'un bateau de pêcheur, ce dernier est délabré.")
        self.rooms.append(fishing_boat)
        fishermans_hut= Room("Fishermans_hut", "dans une cabane de pêcheur, elle semble abandonée.")
        self.rooms.append(fishermans_hut)
        coast= Room("coast", "arrivé sur une côte, une terrez s'étend a perte de vu.")
        self.rooms.append(coast)
        waterfall = Room("Waterfall", "au pied d'une cascade, l'eau s'écrase bruyamment sur les rochers.")
        self.rooms.append(waterfall)
        ascent = Room("Ascent", "sur un chemin qui monte abruptement, le souffle commence à manquer.")
        self.rooms.append(ascent)
        footpath = Room("Footpath", "sur un petit sentier bien tracé, la nature est calme et apaisante.")
        self.rooms.append(footpath)
        crossroads = Room("Crossroads", "à un carrefour de sentiers, plusieurs directions s'offrent à vous.")
        self.rooms.append(crossroads)
        viewpoint = Room("Viewpoint", "à un point de vue élevé, le paysage s'étend majestueusement à l'horizon.")
        self.rooms.append(viewpoint)
        cave_entrance = Room("Cave_entrance", "devant l'entrée d'une sombre caverne, l'air y est frais et humide.")
        self.rooms.append(cave_entrance)
        waterfall_cave = Room("Waterfall_cave", "dans une caverne derrière la cascade, le bruit est assourdissant.")
        self.rooms.append(waterfall_cave)
        path = Room("Sentier", "sur un sentier étroit, la végétation est dense et luxuriante.")
        self.rooms.append(path)
        cliff_top = Room("Cliff_top", "au sommet d'une falaise, le vent est puissant et le vide impressionnant.")
        self.rooms.append(cliff_top)
        little_forest = Room("Little_forest", "dans un petit bois, les arbres sont jeunes et rapprochés.")
        self.rooms.append(little_forest)
        road = Room("road", "sur un sentier étroit et caillouteux, il monte vers une structure en hauteur.")
        self.rooms.append(road)
        castle_entrance = Room("Castle_entrance", "devant la grande porte d'un château en ruines, des gargouilles vous observent.")
        self.rooms.append(castle_entrance)
        dungeon = Room("Dungeon", "dans un cachot sombre et froid, l'air sent la moisissure et le désespoir.")
        self.rooms.append(dungeon)
        bedroom = Room("Bedroom", "dans une chambre poussiéreuse et luxueuse, le temps semble s'être arrêté.")
        self.rooms.append(bedroom)
        boss_s_office = Room("Boss_s_office", "dans un grand bureau, un fauteuil en cuir massif fait face à une cheminée éteinte.")
        self.rooms.append(boss_s_office)
        bridge = Room("Bridge", "sur un pont de pierre fragile, il enjambe un profond ravin.")
        self.rooms.append(bridge)
        balcony = Room("Balcony", "sur un balcon en ruine, vous avez une vue plongeante sur la cour intérieure du château.")
        self.rooms.append(balcony)
        plain = Room("Plain", "dans une vaste plaine herbeuse, le ciel est immense et dégagé.")
        self.rooms.append(plain)
        plateau = Room("Plateau", "sur un plateau rocheux, la végétation est rase et le vent glacial.")
        self.rooms.append(plateau)
        cave = Room("Cave", "dans une cave, une énorme pierre vous tombe dessus")
        self.rooms.append(cave)

        # Create exits for rooms

        crossing.exits = {"N" : little_forest, "E" : meadow, "S" : cave, "O" : waterfall}
        meadow.exits = {"N" : None, "E" : lake, "S" : forest, "O" : crossing}
        forest.exits = {"N" : meadow, "E" : marshes, "S" : None, "O" : None}
        marshes.exits = {"N" : lake, "E" : fishermans_hut, "S" : None, "O" : forest}
        lake.exits = {"N" : None, "E" : fishing_boat, "S" : marshes, "O" : meadow}
        fishing_boat.exits = {"N" : coast, "E" : None, "S" : fishermans_hut, "O" : None}
        fishermans_hut.exits = {"N" : fishing_boat, "E" : None, "S" : None, "O" : marshes}
        coast.exits = {"N" : None, "E" : None, "S" : fishing_boat, "O" : road}
        waterfall.exits = {"N" : ascent, "E" : crossing, "S" : footpath, "O" : waterfall_cave}
        ascent.exits = {"N" : None, "E" : None, "S" : waterfall, "O" : viewpoint}
        footpath.exits = {"N" : waterfall, "E" : None, "S" : None, "O" : crossroads}
        viewpoint.exits = {"N" : None, "E" : ascent, "S" : crossroads, "O" : path}
        path.exits = {"N" : cliff_top, "E" : viewpoint, "S" : waterfall_cave, "O" : None}
        waterfall_cave.exits = {"N" : path, "E" : waterfall, "S" : cave_entrance, "O" : None}
        cave_entrance.exits = {"N" : waterfall_cave, "E" : crossroads, "S" : None, "O" : None}
        cliff_top.exits = {"N" : None, "E" : road, "S" : path, "O" : None}
        road.exits = {"N" : castle_entrance, "E" : coast, "S" : little_forest, "O" : cliff_top}
        little_forest.exits = {"N" : road, "E" : None, "S" : crossing, "O" : None}
        castle_entrance.exits = {"N" : boss_s_office, "E" : dungeon, "S" : road, "O" : bedroom}
        boss_s_office.exits = {"N" : None, "E" : bridge, "S" : road, "O" : balcony}
        dungeon.exits = {"N" : bridge, "E" : None, "S" : None, "O" : castle_entrance}
        bedroom.exits = {"N" : balcony, "E" : castle_entrance, "S" : None, "O" : None}
        balcony.exits = {"N" : None, "E" : boss_s_office, "S" : bedroom, "O" : plateau}
        plateau.exits = {"N" : None, "E" : balcony, "S" : None, "O" : None}
        plain.exits = {"N" : None, "E" : None, "S" : None, "O" : bridge}
        cave.exits = {"N" : crossing, "E" : None, "S" : None, "O" : None}


        syn = {'N':('n','nord','NORD','Nord'),'E':('e','est','EST','Est'),'S':('s','sud','SUD','Sud'),'O':('o','ouest','OUEST','Ouest')}
        for r in (crossing, meadow, forest, marshes, lake, fishing_boat, fishermans_hut, coast, 
                  waterfall, ascent, footpath, crossroads, viewpoint, cave_entrance, 
                  waterfall_cave, path, cliff_top, little_forest, road, castle_entrance, dungeon, 
                  bedroom, boss_s_office, bridge, balcony, plain, plateau, cave): [r.exits.update({s:v for s in (syn.get(k,())+(k.lower(),k.capitalize(),k.upper()))}) for k,v in list(r.exits.items())]

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = crossing

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word == "":
            return
        elif command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
