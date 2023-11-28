
from game import location
#There is some pretense that the game might not be played over the term
#So we use a custim function announce to print things instead of print
from game.display import announce
import game.config as config
import game.items as item
from game.events import *
class DemoIsland(location.Location):
#Demo Island inherits from location
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        #Object handling. Super() refers tp the parent class
        #(Location in this case)
        #So this runs the initializer of Location
        self.name = "island"
        self.symbol = 'I' #Symbol for map
        self.visitable = True #Marks the island as a place the pirates can go ashore
        self.locations = {} #Dictionary of sub-locations on the island
        self.locations["beach"] = Beach(self)
        self.locations["trees"] = Trees(self)
        #Where do the pirates start?
        self.starting_location = self.locations["beach"]

    def enter(self, ship):
        #What to do when the ship visits this loc on the map
        announce("arrived at an island")

    def visit(self):
    #Boilerplate code for starting a visit
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

#Sub-locations (Beach and Trees)
class Beach(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        #The verbs dict was set up by the super() init
        #"go north" has handling that causes sublocations to
        #just get the direction
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter(self):
        announce("You arrived at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb(self, verb, cmd_list, nouns):
        #one of the core functions. contains handling for everything that the player can do here
        #More complex actions should have dedicated functions to handle them
        if (verb == "south"):
            announce("You returned to your ship.")
            #boilerplate code that stops the visit:
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
            #text will be printed by "enter" in Trees()
        if (verb == "east" or verb == "west"):
            announce("You walked all the way around the island on the beach. It's not very interesting.")


class Tress(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "trees"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        #add some treasure
        self.verbs["take"] = self
        self.item_in_tree = Saber()
        self.item_in_clothes = item.Flintlock()
        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkies())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter(self):
        description = "You walk into the small forest on the island."
        if self.item_in_tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + (" in a pile of shredded clothes on the forest floor.")
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb in ["north", "south", "east", "west"]):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if (verb == "take"):
            if (self.item_in_tree == None and self.item_in_clothes == None):
                announce("You don't see anything to take.")
            #they just typed take
            elif (len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False
                item_locs = [self.item_in_tree, self.item_in_clothes]
                i = self.item_in_tree
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " + i.name)
                    config.the_player.add_to_inventory(i)
                    self.item_in_tree = None
                    #this command uses time
                    config.the_player.go = True
                    at_least_one = True
                i = self.item_in_clothes
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " + i.name + " out of the pile of clothes...it looks like someone was eaten here.")
                    config.the_player.add_to_inventory(i)
                    self.item_in_clothes = None
                    # this command uses time
                    config.the_player.go = True
                    at_least_one = True
            if not at_least_one:
                announce("You don't see one of those around.")

class Saber(items.Item):
    def __init__(self):
        super().__init__("saber", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

