from game import location
from game.display import announce
import game.config as config
import game.items as item
from game.events import *
import random


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
                    config.the_player.go = True
                    at_least_one = True
                i = self.item_buried_2
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " + i.name + " out of the sand.")
                    config.the_player.add_to_inventory(i)
                    self.item_buried_2 = None
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
            config.the_player.next_loc = self.main_location.locations["north-cave-deeper"]
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["forest"]


class NorthCaveDeeper(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "north-cave-deeper"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["take"] = self
        self.treasurechest = TreasureChest()

    def enter(self):
        if self.treasurechest is None:
            announce("You have gone deeper into the cave but there is nothing else here.")
        elif self.treasurechest == TreasureChest():
            announce("You have gone deeper into the cave. It's dark but you can make out the shape of a Treasure Chest!")

    def process_verbs(self, verb, cmd_list, nouns):
        if verb == "east" or verb == "west":
            announce("You can't go this direction from here.")
        if verb == "north":
            announce("You cannot go deeper into this cave.")
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["north-cave"]
        if verb == "take":
            if self.treasurechest is None:
                announce("You don't see anything to take.")
            if self.treasurechest == TreasureChest():
                announce("You found treasure!")
                config.the_player.add_to_inventory(TreasureChest())
                self.treasurechest = None


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
            config.the_player.next.loc = self.main_location.locations["west-cave-deeper"]


class WestCaveDeeper(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "west-cave-deeper"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.treasure = SmallTreasure()

    def enter(self):
        if self.treasure == SmallTreasure():
            announce("You have gone deeper into the cave. There is some treasure on the ground and "
                     "it looks like there is a message on the wall above. It says... I am east of here, "
                     "but south of south, I am hidden in the dark even when it's day.")
        elif self.treasure is None:
            announce("You have gone deeper into the cave. The message on the wall still says...I am east of here, "
                     "but south of south, I am hidden in the dark even when it's day. There is nothing else here.")

    def process_verbs(self, verb, cmd_list, nouns):
        if verb == "north" or verb == "south":
            announce("You can't go that direction from here.")
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["west-cave"]
        if verb == "west":
            announce("You cannot go deeper into this cave. It is a dead end.")
        if verb == "take":
            if self.treasure is None:
                announce("You don't see anything to take.")
            if self.treasure == SmallTreasure():
                announce("You found treasure!")
                config.the_player.add_to_inventory(SmallTreasure())
                self.treasure = None


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
        self.treasure = Treasure()

    def monster_attack(self, combat):
        result = {}
        result["message"] = "the drowned pirates are defeated!"
        monsters = []
        min = 2
        uplim = 6
        if random.randrange(2) == 0:
            min = 1
            uplim = 5
            monsters.append(combat.Drowned("Pirate captain"))
            monsters[0].speed = 1.2 * monsters[0].speed
            monsters[0].health = 2 * monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.Drowned("Drowned pirate " + str(n)))
            n += 1
        announce("You are attacked by a crew of drowned pirates!")
        combat.Combat(monsters).combat()
        result["newevents"] = [self]
        return result

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


class TreasureChest(item.Item):
    def __init__(self):
        super().__init__("treasurechest", 500)
        self.value = 500


class Treasure(item.Item):
    def __init__(self):
        super().__init__("treasure", 100)
        self.value = 100


class SmallTreasure(item.Item):
    def __init__(self):
        super().__init__("smalltreasure", 50)
        self.value = 50
