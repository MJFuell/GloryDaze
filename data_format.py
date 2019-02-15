'''
data_format.py
Data format development for GloryDaze Text Adventure
by: Richard Ratliff

CS467
Winter 2019
Team Keid :: Michael Fuelling, Richard Ratliff, Jordan Riojas
'''

import glob
import json

import util

# DELAY = 0.001   # make this smaller for a faster scroll
DELAY = 0       # make this smaller for a faster scroll
MAXLEN = 80     # maximum line length to print

'''
    Build Exit objects for the game from JSON files found in a directory.
    Read json files in exits data directory and create an Exit object from each.
    Return a list of Exit objects.
    '''
class ExitBuilder:
    
    def __init__(self):
        pass
    
    '''
    Read json files in exits data directory and create an Exit object from each.
    Return a list of Exit objects.
    '''
    def load_exit_files(self, dir="./data/exits/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            # print("file: ", file)
            with open(file) as exit:
                exit_props = json.load(exit)
                new_exit = Exit(exit_props)
                #util.scroll(DELAY, MAXLEN, "Created Exit '{}' from {}".format(new_exit.get_name(), file))
                list.append(new_exit)
        return list

'''
Exit object model. Attributes and methods for each exit of a room.
'''
class Exit:

    def __init__(self, props):
        self.name  = props["name"]         # name of exit
        self.long  = props["long"]         # long description
        self.short = props["short"]        # short description
        self.save()                        # save the new object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "---------")
        util.scroll3(DELAY, MAXLEN, "Exit Info")
        util.scroll3(DELAY, MAXLEN, "---------")
        util.scroll3(DELAY, MAXLEN, "Name:    {}".format(self.get_name()))
        util.scroll3(DELAY, MAXLEN, "Long:    {}".format(self.get_long()))
        util.scroll3(DELAY, MAXLEN, "Short:   {}".format(self.get_short()))

    def get_name(self):
        return self.name

    def get_long(self):
        return self.long

    def get_short(self):
        return self.short

'''
Build Room objects for the game from JSON files found in a directory.
Read json files in rooms data directory and create a Room object from each.
Return a list of Room objects.
'''
class RoomBuilder:

    def __init__(self):
        pass

    '''
    Read json files in rooms data directory and create a Room object from each.
    Return a list of Room objects.
    '''
    def load_room_files(self, dir="./data/rooms/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            # print("file: ", file)
            with open(file) as room:
                room_props = json.load(room)
                new_room = Room(room_props)
                #util.scroll(DELAY, MAXLEN, "Created Room '{}' from {}".format(new_room.get_name(), file))
                list.append(new_room)
        return list

'''
Room object model. Attributes and methods for each room.
'''
class Room:
    def __init__(self, props):
        self.name        = props["name"]         # name of room like Cafeteria
        self.altnames    = props["altnames"]     # alternate name(s) like Cafe or Lunchroom
        self.long        = props["long"]         # long description
        self.short       = props["short"]        # short description
        self.addl        = props["addl"]         # additional something that happens when in the room
        self.exits       = props["exits"]        # dictionary of exit directions and name of the room
        self.items       = props["items"]        # list of items in the room
        self.visited     = props["visited"]      # STATE - True/False - has player visited the room
        self.save()                              # save the new object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "---------")
        util.scroll3(DELAY, MAXLEN, "Room Info")
        util.scroll3(DELAY, MAXLEN, "---------")
        util.scroll3(DELAY, MAXLEN, "Name:    {}".format(self.get_name()))
        for altname in self.get_altnames():
            util.scroll3(DELAY, MAXLEN, "AltName: {}".format(altname))
        util.scroll3(DELAY, MAXLEN, "Long:    {}".format(self.get_long()))
        util.scroll3(DELAY, MAXLEN, "Short:   {}".format(self.get_short()))
        util.scroll3(DELAY, MAXLEN, "Addl:    {}".format(self.get_addl()))
        exits = self.get_exits()
        for exit, room in exits.items():
            util.scroll3(DELAY, MAXLEN, "Exit Direction : {}".format(exit))
            util.scroll3(DELAY, MAXLEN, "Exit Next Room : {}".format(room))
            # util.scroll3(DELAY, MAXLEN, "{} : {}".format(exit, exits[exit])) # ok but ugly syntax
            util.scroll3(DELAY, MAXLEN, "{} : {}".format(exit, room))
        for item in self.get_items():
            util.scroll3(DELAY, MAXLEN, "Item:    {}".format(item))
        util.scroll3(DELAY, MAXLEN, "Visited:  {}".format(self.get_visited()))

    def get_name(self):
        return self.name

    def get_altnames(self):
        return self.altnames

    def get_long(self):
        return self.long

    def get_short(self):
        return self.short

    def get_addl(self):
        return self.addl

    def get_exitdirs(self):
        return self.exitdirs

    def get_exits(self):
        return self.exits

    def get_items(self):
        return self.items

    def drop_item(self, value):
        self.items.append(value)

    def take_item(self, value):
        self.items.remove(value)

    def get_visited(self):
        return self.visited

'''
Build Item objects for the game from JSON files found in a directory.
Read json files in items data directory and create an Item object from each.
Return a list of Item objects.
'''
class ItemBuilder:

    def __init__(self):
        pass

    '''
    Read all json files in the items data directory and create Item objects.
    Return a list of Item objects.
    '''
    def load_item_files(self, dir="./data/items/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            # print("file: ", file)
            with open(file) as item:
                item_props = json.load(item)
                new_item = Item(item_props)
                #util.scroll(DELAY, MAXLEN, "Created Item '{}' from {}".format(new_item.get_name(), file))
                list.append(new_item)
        return list

'''
Item object model. Attributes and methods for each item.
'''
class Item:
    def __init__(self, props):
        self.name        = props["name"]         # name of item like phone
        self.altnames    = props["altnames"]     # alternate name(s) like cell and cellphone
        self.long        = props["long"]         # long description
        self.featFalse   = props["featureFalse"] # extra item feature description, like backpack has a tear
        self.featBool    = props["featureBool"]  # feature description boolean
        self.featTrue    = props["featureTrue"]  # extra item feature description, like backpack was fixed
        self.short       = props["short"]        # short description
        self.have        = props["have"]         # text to print when player acquires item
        self.available   = props["available"]    # text to print when player looks and item is available
        self.take        = props["take"]         # text to print when player takes the item
        self.drop        = props["drop"]         # text to print when player drops the item
        self.havenot     = props["havenot"]      # ERROR - player tried to use item they do not have
        self.unavailable = props["unavailable"]  # ERROR - player tried to take item when unavailable
        self.save()                              # save the new object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "---------")
        util.scroll3(DELAY, MAXLEN, "Item Info")
        util.scroll3(DELAY, MAXLEN, "---------")
        util.scroll3(DELAY, MAXLEN, "Name:    {}".format(self.get_name()))
        for altname in self.get_altnames():
            util.scroll3(DELAY, MAXLEN, "AltName: {}".format(altname))
        util.scroll3(DELAY, MAXLEN, "Long:    {}".format(self.get_long()))
        util.scroll3(DELAY, MAXLEN, "FeatF:   {}".format(self.get_feat_false()))
        util.scroll3(DELAY, MAXLEN, "FeatB:   {}".format(self.get_feat_bool()))
        util.scroll3(DELAY, MAXLEN, "FeatT:   {}".format(self.get_feat_true()))
        util.scroll3(DELAY, MAXLEN, "Short:   {}".format(self.get_short()))
        util.scroll3(DELAY, MAXLEN, "Have:    {}".format(self.get_have()))
        util.scroll3(DELAY, MAXLEN, "HaveNot: {}".format(self.get_havenot()))
        util.scroll3(DELAY, MAXLEN, "Avail:   {}".format(self.get_avail()))
        util.scroll3(DELAY, MAXLEN, "Unavail: {}".format(self.get_unavail()))
        util.scroll3(DELAY, MAXLEN, "Take:    {}".format(self.get_take()))
        util.scroll3(DELAY, MAXLEN, "Drop:    {}".format(self.get_drop()))

    def set_feat_bool(self, value):
        self.featBool = value

    def get_name(self):
        return self.name

    def get_altnames(self):
        return self.altnames

    def get_long(self):
        return self.long

    def get_feat_false(self):
        return self.featFalse

    def get_feat_bool(self):
        return self.featBool

    def get_feat_true(self):
        return self.featTrue

    def get_short(self):
        return self.short

    def get_have(self):
        return self.have

    def get_havenot(self):
        return self.havenot

    def get_avail(self):
        return self.available

    def get_unavail(self):
        return self.unavailable

    def get_take(self):
        return self.take

    def get_drop(self):
        return self.drop

'''
Build Character objects for the game from JSON files found in a directory.
Read all json files in the chars data directory and create Character objects.
Return a list of Character objects.
'''
class CharacterBuilder:

    def __init__(self):
        pass

    '''
    Read all json files in the chars data directory and create Character objects.
    Return a list of Character objects.
    '''
    def load_char_files(self, dir="./data/chars/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            # print("file: ", file)
            with open(file) as char:
                char_props = json.load(char)
                new_char = Character(char_props)
                #util.scroll(DELAY, MAXLEN, "Created Character '{}' from {}".format(new_char.get_name(), file))
                list.append(new_char)
        return list

'''
Character object model. Attributes and methods for each character.
'''
class Character:
    def __init__(self, props):
        self.name        = props["name"]         # name of item like phone
        self.long        = props["long"]         # long description
        self.short       = props["short"]        # short description
        self.hint        = props["hint"]         # hint to share with player
        self.save()                              # save the new object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "--------------")
        util.scroll3(DELAY, MAXLEN, "Character Info")
        util.scroll3(DELAY, MAXLEN, "--------------")
        util.scroll3(DELAY, MAXLEN, "Name:  {}".format(self.get_name()))
        util.scroll3(DELAY, MAXLEN, "Long:  {}".format(self.get_long()))
        util.scroll3(DELAY, MAXLEN, "Short: {}".format(self.get_short()))
        util.scroll3(DELAY, MAXLEN, "Hint:  {}".format(self.get_hint()))

    def get_name(self):
        return self.name

    def get_long(self):
        return self.long

    def get_short(self):
        return self.short

    def get_hint(self):
        return self.hint

'''
Player object and methods. There is only one player object.
There is no builder to create Players.
'''
class Player:
    def __init__(self):
        self.name        = "Player1"   # name of the player starting with Player1
        self.location    = "Detention" # location of the player on the map starting in Detention.
        self.items       = []          # items collected in inventory
        # self.timeleft    = props["timeleft"]
        self.save()                    # save the new object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "-----------")
        util.scroll3(DELAY, MAXLEN, "Player Info")
        util.scroll3(DELAY, MAXLEN, "-----------")
        util.scroll3(DELAY, MAXLEN, "Name:     {}".format(self.get_name()))
        util.scroll3(DELAY, MAXLEN, "Location: {}".format(self.get_location()))
        for item in self.get_items():
            util.scroll3(DELAY, MAXLEN, "Item:     {}".format(item))

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_location(self):
        return self.location

    def set_location(self, value):
        self.location = value

    def get_items(self):
        return self.items

    def add_item(self, value):
        self.items.append(value)

    def drop_item(self, value):
        self.items.remove(value)


'''
main() handles the following test code printing out the objects created.
when imported into another python module main() will not execute.
main() illustrates how to use the classes and some util functions.
'''
def main():

    ''' Make a Builder object and use it to load json data files to create a list of underlying game objects '''

    exit_builder = ExitBuilder()
    exit_list = ExitBuilder.load_exit_files(exit_builder)

    room_builder = RoomBuilder()
    room_list = RoomBuilder.load_room_files(room_builder)

    item_builder = ItemBuilder()
    item_list = ItemBuilder.load_item_files(item_builder)

    char_builder = CharacterBuilder()
    character_list = CharacterBuilder.load_char_files(char_builder)

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "print me - object.print_me()")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    player = Player()
    player.print_me()

    player.set_name("Pat")
    player.set_location("Main Office")
    player.add_item("metronome")
    player.add_item("calculator")
    player.add_item("master key")

    player.print_me()

    ''' Loop through all the lists to do things like print_me() '''
    for exit in exit_list:
        exit.print_me()
    
    for room in room_list:
        room.print_me()
    
    for item in item_list:
        item.print_me()
    
    for character in character_list:
        character.print_me()

    quit()
    quit()
    quit()
    quit()
    quit()
    quit()

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for thing in list print thing.attributes")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    for room in room_list:
        print("printing ... room info ...")
        print("Name:   ", room.get_name())
        print("Long:   ", room.get_long())
        print("Short:  ", room.get_short())
        print("Addl:   ", room.get_addl())
        exits = room.get_exits()
        for exit, nextroom in exits.items():
            print("Exit Direction : {}".format(exit))
            print("Exit Next Room : {}".format(nextroom))
            print("{} : {}".format(exit, nextroom))
        print("Visited: ", room.get_visited())

    for item in item_list:
        print("printing ... item info ...")
        print("Name:   ", item.get_name())
        for altname in item.get_altnames():
            print("AltName:", altname)
        print("Long:   ", item.get_long())
        print("FeatF:  ", item.get_feat_false())
        print("FeatB:  ", item.get_feat_bool())
        print("FeatT:  ", item.get_feat_true())
        print("Short:  ", item.get_short())
        print("Have:   ", item.get_have())
        print("HaveNot:", item.get_havenot())
        print("Avail:  ", item.get_avail())
        print("Unavail:", item.get_unavail())
        print("Take:   ", item.get_take())
        print("Drop:   ", item.get_drop())
        item.save()

    for char in character_list:
        print("printing ... character info ...")
        print("Name:   ", char.get_name())
        print("Long:   ", char.get_long())
        print("Short:  ", char.get_short())
        print("Hint:   ", char.get_hint())

    print("printing ... player info ...")
    print("Name:    ", player.get_name())
    print("Location:", player.get_location())
    for item in player.get_items():
        print("Item:    ", item)

if __name__ == '__main__':
    main()
