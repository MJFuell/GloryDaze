'''
data.py
Description: Data structure classes
Principal author per project plan: Richard Ratliff

CS467
Winter 2019
Team Keld :: Michael Fuelling, Richard Ratliff, Jordan Riojas
GloryDaze Text Adventure
'''

import glob
import json

import util

DELAY = 0.01
MAXLEN = 80

class RoomBuilder:
    '''
    Builds the rooms of the game
    '''
    def __init__(self):
        pass

    def load_room_files(self, dir="./data/rooms/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            with open(file) as room:
                room_props = json.load(room)
                new_room = Room(room_props)
                util.scroll(DELAY, MAXLEN, "Building Room '{}'".format(new_room.get_name()))
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
            util.scroll3(DELAY, MAXLEN, "{} : {}".format(exit, exits[exit]))
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

class Character:
    def __init__(self, name):
        self.name = name
        util.scroll(DELAY, MAXLEN, "constructed a character")

    def get_name(self):
        return self.name

    def print_stats(self):
        util.scroll(DELAY, MAXLEN, "Character Info")
        util.scroll(DELAY, MAXLEN, "Name: {}".format(self.name))

    def save(self):
        util.save(self)

class ItemBuilder:
    '''
    Builds the items that have an effect on game outcome
    '''
    def __init__(self):
        pass

    def load_item_files(self, dir="./data/items/*.json"):
        files = glob.glob(dir)
        list = []
        for file in files:
            with open(file) as item:
                item_props = json.load(item)
                new_item = Item(item_props)
                util.scroll(DELAY, MAXLEN, "Building Item '{}'".format(new_item.get_name()))
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

def main():
    # util.scroll/3 used here in main() and in RoomBuilder and Room.print_me()
    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "RoomBuilder")
    util.scroll(DELAY, MAXLEN, "-" * 80)
    room_builder = RoomBuilder()
    room_list = RoomBuilder.load_room_files(room_builder)
    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for rooms in room list room.print_me()")
    util.scroll(DELAY, MAXLEN, "-" * 80)
    for room in room_list:
        room.print_me()
    # util.scroll/3 used here in main() and in ItemBuilder and Item.print_me()
    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "ItemBuilder")
    util.scroll(DELAY, MAXLEN, "-" * 80)
    ib = ItemBuilder()
    item_list = ItemBuilder.load_item_files(ib)
    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for items in item list item.print_me()")
    util.scroll(DELAY, MAXLEN, "-" * 80)
    for item in item_list:
        item.print_me()
    util.scroll(DELAY, MAXLEN, "-" * 80)
    util.scroll(DELAY, MAXLEN, "for items in item list print item.get_stuff() ..................................")
    util.scroll(DELAY, MAXLEN, "-" * 80)
    # just print the reset to speed things up
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
