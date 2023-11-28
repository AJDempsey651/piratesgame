from game import location
from game.display import announce
import game.config as config
import game.items as item
from game.events import *


class CaveIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "Cave Island"
        self.symbol = "CI"
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach(self)
        self.locations["forest"] = Forest(self)
        self.locations["north-cave"] = NorthCave(self)
        self.locations["west-cave"] = WestCave(self)
        self.locations["lagoon"] = Lagoon(self)
        self.starting_location = self.locations["beach"]

    def enter(self, ship):
        announce("You have arrived at an island.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class Beach(location.SubLocation):

    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["take"] = self
        self.item_buried = item.Flintlock()
        self.item_buried_2 = item.Cutlass()
        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter(self):
        announce("You have arrived at a beach. Your ship is anchored to your east.")
        announce("There is a thick forest to your west.")
        announce("The beach continues along the coast to your north and south.")
        announce("You see a " + self.item_buried + " and a " + self.item_buried_2 + " partially buried in the sand.")

    def process_verbs(self, verb, cmd_list, nouns):
        if verb == "east":
            announce("You have returned to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if verb == "north" or verb == "south":
            announce("There is nothing but beach in that direction.")
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "take":
            if self.item_buried is None and self.item_buried_2 is None:
                announce("You don't see anything to take.")
            elif (len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False
                item_locs = [self.item_buried, self.item_buried_2]
                i = self.item_buried
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " + i.name + " out of the sand.")
                    config.the_player.add_to_inventory(i)
                    self.item_buried = None
                    #this command uses time
                    config.the_player.go = True
                    at_least_one = True
                i = self.item_buried_2
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " + i.name + " out of the sand.")
                    config.the_player.add_to_inventory(i)
                    self.item_buried_2 = None
                    # this command uses time
                    config.the_player.go = True
                    at_least_one = True
            if not at_least_one:
                announce("You don't see one of those around.")



class Forest(location.SubLocation):

    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "forest"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.event_chance = 25
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(sickness.Sickness())

    def enter(self):
        announce("You have entered a large, thick forest.")
        announce("There appears to be thin trails to your west, north and south.")

    def process_verbs(self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["north-cave"]
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["west-cave"]
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["lagoon"]


class NorthCave(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "north-cave"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.event_chance = 95
        self.events.append(man_eating_monkeys.ManEatingMonkeys)

    def enter(self):
        announce("You have entered a cave on the north side of the island. Careful, it's dark.")
        announce("It appears that something may be living in this cave.")

    def process_verbs(self, verb, cmd_list, nouns):
        if verb == "east" or verb == "west":
            announce("You can't go this direction from here.")
        if verb == "north":
            announce("You walked all the way to the end of the cave. There is nothing else here.")
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["forest"]


class WestCave(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "west-cave"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self

    def enter(self):
        announce("You have entered a cave on the west side of the island. Careful, it's dark.")

    def process_verbs(self, verb, cmd_list, nouns):
        if verb == "north" or verb == "south":
            announce("You can't go that direction from here.")
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "west":
            announce("You have walked all the way to the end of the cave. There is nothing else in there.")


class Lagoon(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "lagoon"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["take"] = self
        self.item_floating = item.Cutlass()
        self.event_chance = 50
        self.events.append(drowned_pirates.DrownedPirates())

    def enter(self):
        description = ("You have arrived at a lagoon in the forest on the south end of the island.")
        if self.item_floating != None:
            description = description + "You see a " + self.item_floating + " floating on the edge of the lagoon"
        announce(description)

    def process_verbs(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "south":
            announce("You can't go through the lagoon. You don't know how to swim!")
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "take":
            if self.item_floating is None:
                announce("You don't see anything to take.")
            if self.item_floating == item.Cutlass():
                announce("You picked up a cutlass")
                config.the_player.add_to_inventory(item.Cutlass())
                self.item_floating = None

