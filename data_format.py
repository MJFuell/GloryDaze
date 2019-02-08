'''
data_format.py
Data format development for GloryDaze Text Adventure
by: Richard Ratliff

CS467
Winter 2019
Team Keld :: Michael Fuelling, Richard Ratliff, Jordan Riojas

class Player:
    Player object and methods. There is only one player object.
    Data attributes are:
        name # name of the player starting with Player1
        location # location of the player on the map starting in Detention.
        items # items collected in inventory
class CharacterBuilder:
    Build Character objects for the game from JSON files found in a directory.
    Read all json files in the chars data directory and create Character objects.
    Returns a list of Character objects.
class Character:
    Character object model. Attributes and methods for each character.
    Data attributes are:
        name # name of item like phone
        long # long description
        short # short description
        hint # hint to share with player
class RoomBuilder:
    Build Room objects for the game from JSON files found in a directory.
    Read json files in rooms data directory and create a Room object from each.
    Returns a list of Room objects.
class Room:
    Room object model. Attributes and methods for each room.
    Data attributes are:
        name # name of room like Cafeteria
        altnames # alternate name(s) like Cafe or Lunchroom
        long # long description
        short # short description
        addl # additional something that happens when in the room
        exits # dictionary of exit directions and name of the room
        visited # STATE - True/False - has player visited the room
class ItemBuilder:
    Build Item objects for the game from JSON files found in a directory.
    Read json files in items data directory and create an Item object from each.
    Returns a list of Item objects.
class Item:
    Item object model. Attributes and methods for each item.
    Data attributes are:
        name # name of item like phone
        altnames # alternate name(s) like cell and cellphone
        long # long description
        short # short description
        start # location (room) at the start of a new game
        have # text to print when player acquires item
        available # text to print when player looks and item is available
        take # text to print when player takes the item
        drop # text to print when player drops the item
        current # STATE - current location of item, will be start unless moved by player
        havenot # ERROR - player tried to use item they do not have
        unavailable # ERROR - player tried to take item when unavailable
main() contains test code printing out the objects created.
    when imported into another python module main() will not execute.
    main() illustrates how to use the classes and some util functions.
'''

import glob
import json

import util

DELAY = 0.005
MAXLEN = 80

class RoomBuilder:
    '''
    Build Room objects for the game from JSON files found in a directory.
    '''
    def __init__(self):
        pass

    '''
    Read json files in rooms data directory and create a Room object from each.
    Returns a list of Room objects.
    '''
    def load_room_files(self, dir="./data/rooms/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            with open(file) as room:
                room_props = json.load(room)
                new_room = Room(room_props)
                util.scroll(DELAY, MAXLEN, "Building Room '{}' from {}".format(new_room.get_name(), file))
                list.append(new_room)
        return list

class Room:
    def __init__(self, props):
        self.name        = props["name"]         # name of room like Cafeteria
        self.altnames    = props["altnames"]     # alternate name(s) like Cafe or Lunchroom
        self.long        = props["long"]         # long description
        self.short       = props["short"]        # short description
        self.addl        = props["addl"]         # additional something that happens when in the room
        self.exits       = props["exits"]        # dictionary of exit directions and name of the room
        self.visited     = props["visited"]      # STATE - True/False - has player visited the room
        self.save()                              # save the new item object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "-" * 80)
        util.scroll3(DELAY, MAXLEN, "Room Info")
        util.scroll3(DELAY, MAXLEN, "-" * 80)
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

    def get_visited(self):
        return self.visited

class ItemBuilder:
    '''
    Build Item objects for the game from JSON files found in a directory.
    '''
    def __init__(self):
        pass

    '''
    Read all json files in the items data directory and create Item objects.
    Returns a list of Item objects.
    '''
    def load_item_files(self, dir="./data/items/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            with open(file) as item:
                item_props = json.load(item)
                new_item = Item(item_props)
                util.scroll(DELAY, MAXLEN, "Building Item '{}' from {}".format(new_item.get_name(), file))
                list.append(new_item)
        return list

class Item:
    def __init__(self, props):
        self.name        = props["name"]         # name of item like phone
        self.altnames    = props["altnames"]     # alternate name(s) like cell and cellphone
        self.long        = props["long"]         # long description
        self.short       = props["short"]        # short description
        self.start       = props["start"]        # location (room) at the start of a new game
        self.have        = props["have"]         # text to print when player acquires item
        self.available   = props["available"]    # text to print when player looks and item is available
        self.take        = props["take"]         # text to print when player takes the item
        self.drop        = props["drop"]         # text to print when player drops the item
        self.current     = props["current"]      # STATE - current location is start unless moved by player
        self.havenot     = props["havenot"]      # ERROR - player tried to use item they do not have
        self.unavailable = props["unavailable"]  # ERROR - player tried to take item when unavailable
        self.save()                              # save the new item object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "-" * 80)
        util.scroll3(DELAY, MAXLEN, "Item Info")
        util.scroll3(DELAY, MAXLEN, "-" * 80)
        util.scroll3(DELAY, MAXLEN, "Name:    {}".format(self.get_name()))
        for altname in self.get_altnames():
            util.scroll3(DELAY, MAXLEN, "AltName: {}".format(altname))
        util.scroll3(DELAY, MAXLEN, "Long:    {}".format(self.get_long()))
        util.scroll3(DELAY, MAXLEN, "Short:   {}".format(self.get_short()))
        util.scroll3(DELAY, MAXLEN, "Start:   {}".format(self.get_start()))
        util.scroll3(DELAY, MAXLEN, "Current: {}".format(self.get_current()))
        util.scroll3(DELAY, MAXLEN, "Have:    {}".format(self.get_have()))
        util.scroll3(DELAY, MAXLEN, "HaveNot: {}".format(self.get_havenot()))
        util.scroll3(DELAY, MAXLEN, "Avail:   {}".format(self.get_avail()))
        util.scroll3(DELAY, MAXLEN, "Unavail: {}".format(self.get_unavail()))
        util.scroll3(DELAY, MAXLEN, "Take:    {}".format(self.get_take()))
        util.scroll3(DELAY, MAXLEN, "Drop:    {}".format(self.get_drop()))

    def get_name(self):
        return self.name

    def get_altnames(self):
        return self.altnames

    def get_long(self):
        return self.long

    def get_short(self):
        return self.short

    def get_start(self):
        return self.start

    def get_current(self):
        return self.current

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

class CharacterBuilder:
    '''
    Build Character objects for the game from JSON files found in a directory.
    '''
    def __init__(self):
        pass

    '''
    Read all json files in the chars data directory and create Character objects.
    Returns a list of Character objects.
    '''
    def load_char_files(self, dir="./data/chars/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            with open(file) as char:
                char_props = json.load(char)
                new_char = Character(char_props)
                util.scroll(DELAY, MAXLEN, "Building Character '{}' from {}".format(new_char.get_name(), file))
                list.append(new_char)
        return list

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
        util.scroll3(DELAY, MAXLEN, "-" * 80)
        util.scroll3(DELAY, MAXLEN, "Character Info")
        util.scroll3(DELAY, MAXLEN, "-" * 80)
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

class Player:
    def __init__(self):
        self.name        = "Player1"
        self.location    = "Detention"
        self.items       = []
        # self.timeleft    = props["timeleft"]
        self.save()                              # save the new object just initialized

    def save(self):
        util.save(self)

    def print_me(self):
        util.scroll3(DELAY, MAXLEN, "-" * 80)
        util.scroll3(DELAY, MAXLEN, "Player Info")
        util.scroll3(DELAY, MAXLEN, "-" * 80)
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

    #TODO def drop_item(self, value):
    #    self.items.append(value)


def main():
    '''
    main() handles the following test code printing out the objects created.
    when imported into another python module main() will not execute.
    main() illustrates how to use the classes and some util functions.
    '''

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "Player defaults")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    player = Player()
    player.print_me()

    print("---- ")
    print("---- Player sets and adds")
    print("---- ")

    player.set_name("Pat")
    player.set_location("Main Office")
    player.add_item("metronome")
    player.add_item("calculator")
    player.add_item("master key")

    player.print_me()

    print("---- ")
    print("---- printing ... player info ...")
    print("---- ")
    print("Name:    ", player.get_name())
    print("Location:", player.get_location())
    for item in player.get_items():
        print("Item:    ", item)

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "CharacterBuilder")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    ''' Make a CharacterBuilder object and use it to load json data files to get a list of Character objects '''
    char_builder = CharacterBuilder()
    character_list = CharacterBuilder.load_char_files(char_builder)

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for characters in character list character.print_me()")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    ''' Loop through all the characters to do things like print_me() '''
    for character in character_list:
        character.print_me()

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for chars in char list print char.get_stuff() ..................................")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    # just print instead of scroll to speed things up
    ''' Loop through all the characters and use get methods '''
    for char in character_list:
        print("printing ... character info ...")
        print("Name:   ", char.get_name())
        print("Long:   ", char.get_long())
        print("Short:  ", char.get_short())
        print("Hint:   ", char.get_hint())

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "RoomBuilder")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    ''' Make a RoomBuilder object and use it to load json data files to get a list of Room objects '''
    room_builder = RoomBuilder()
    room_list = RoomBuilder.load_room_files(room_builder)

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for rooms in room list room.print_me()")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    ''' Loop through all the rooms to do things like print_me() '''
    for room in room_list:
        room.print_me()

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for rooms in room list print room.get_stuff() ..................................")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    # just print instead of scroll to speed things up
    ''' Loop through all the rooms and use get methods '''
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

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "ItemBuilder")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    ''' Make an ItemBuilder object and use it to load json data files to get a list of Item objects '''
    item_builder = ItemBuilder()
    item_list = ItemBuilder.load_item_files(item_builder)

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for items in item list item.print_me()")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    ''' Loop through all the items to do things like print_me() '''
    for item in item_list:
        item.print_me()

    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for items in item list print item.get_stuff() ..................................")
    util.scroll(DELAY, MAXLEN, "-" * 80)

    # just print instead of scroll to speed things up
    ''' Loop through all the items and use get methods '''
    for item in item_list:
        print("printing ... item info ...")
        print("Name:   ", item.get_name())
        for altname in item.get_altnames():
            print("AltName:", altname)
        print("Long:   ", item.get_long())
        print("Short:  ", item.get_short())
        print("Start:  ", item.get_start())
        print("Current:", item.get_current())
        print("Have:   ", item.get_have())
        print("HaveNot:", item.get_havenot())
        print("Avail:  ", item.get_avail())
        print("Unavail:", item.get_unavail())
        print("Take:   ", item.get_take())
        print("Drop:   ", item.get_drop())
        item.save()

if __name__ == '__main__':
    main()
