

import util
import data_format
from parser_files import parser
from parser_files import lexicon


directions = ["north", "south", "east", "west", "northeast", "southeast", "northwest", "southwest"]

err = "Can't do that"

def verb_save(GS, obj):
	pass
	#Save all game info to save files/directory
	#let the user know the game has been saved

def verb_load(GS, obj):
	pass
	#Ask the user if they are sure they want to load as it will overwrite current progress
	#load data into new gamestate
	#call gameLoop() with loaded gamestate

def verb_help(GS, obj):
	pass
	#print help info to the user

def verb_inventory(GS, obj):
	pass
	#display current inventory





def verb_go(GS, obj):

	move = False

	#Room name or alt room name
	#Make sure that room is adjacent
	for x in GS.room_list:
		#print('x.name = ' + x.name)
		#print('x.altnames = ' + ", ".join(str(e) for e in x.altnames))
		if obj == x.name.lower() or obj in x.altnames:
			#print('x is ' + x.name)
			if x.name in GS.current_room.exits.values():
				GS.current_room = x
				move = True

			
	#Directions
	#Make sure you can travel that direction from current room
	if obj in GS.current_room.exits:
		roomName = GS.current_room.exits.get(obj)
		for x in GS.room_list:
			if x.name == roomName:
				GS.current_room = x
				move = True

	#If we successfully moved rooms
	if move == True:
		print('-' * 70, '\n\n\n')
		exits = GS.current_room.get_exits()
		#print('Moved to ' + GS.current_room.get_name())
		util.print_ascii_art('./data/artwk/' + GS.current_room.get_name())
		print('')
		if GS.current_room.visited:
			util.scroll3(0.01, 60, GS.current_room.get_short())
			print('')
			for item in GS.current_room.get_items():
				for x in GS.item_list:
					if x.name == item or item in x.altnames:
						util.scroll3(0.01, 60, "{}".format(x.get_avail()))
						print('')
			for exits_dir, exits_room in exits.items():
				for x in GS.exit_list:
					if x.name == exits_room and exits_dir in directions:
						util.scroll3(0.01, 60, "{} {}".format(x.get_short(),exits_dir))
						print('')
		else:
			util.scroll3(0.01, 60, GS.current_room.get_long())
			print('')
			for item in GS.current_room.get_items():
				for x in GS.item_list:
					if x.name == item or item in x.altnames:
						util.scroll3(0.01, 60, "{}".format(x.get_avail()))
						print('')
			for exits_dir, exits_room in exits.items():
				for x in GS.exit_list:
					if x.name == exits_room and exits_dir in directions:
						util.scroll3(0.01, 60, "{} {}".format(x.get_long(),exits_dir))
						print('')
		GS.current_room.visited = True

	#If we did not move
	else:
		print('Can\'t go that way')
        

def verb_look(GS, obj):
	pass
	#If no object, print long description of room
	#otherwise print description of item

def verb_take(GS, obj):
	pass
	#make sure user has a backpack
	#verify item is in the room
	#add item to inventory if possible




def command(GS, s):
	if s.subject == 'player':

		if s.verb == 'save' or 'savegame':
			verb_save(GS, s.object)

		if s.verb == 'load' or 'loadgame':
			verb_load(GS, s.object)

		if s.verb == 'help':
			verb_help(GS, s.object)

		if s.verb == 'inventory':
			verb_inventory(GS, s.object)



		if s.verb == "go":
			verb_go(GS, s.object)
        
		if s.verb == 'look':
			verb_go(GS, s.object)

		if s.verb == 'take':
			verb_take(GS, s.object)

		

		
		if s.verb == 'talk':
			verb_talk(GS, s.object)

		if s.verb == 'drop':
			verb_drop(GS, s.object)

		if s.verb == 'open':
			verb_open(GS, s.object)

	else:
		print('I Don\'t understand')

'''
backpack - pack bag bookbag
book - harry harrypotter potter harrypotterbook
bottledwater - water bottle coldwater cold water
calculator - calc calcalator calclator
camera - cam gopro
cellphone - cell phone cell phone
ducttape - tape ducttape ducktape
officepass - officepass pass
piccolo - picolo piccollo picollo picalo piccalo
sdcard - sd card sdcard memorycard memory card
'''



