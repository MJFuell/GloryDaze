

import util

directions = ["north", "south", "east", "west", "northeast", "southeast", "northwest", "southwest"]
charRoom = {
    "Gym" : "Coach",
    "Computer Lab" : "LabTeacher",
    "Counselor Office" : "Counselor",
    "Janitor Office" : "Janitor",
    "Library" : "Librarian",
    "Principal Office" : "Principal"
}

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
	#display current inventory
	print('You are currently holding:')
	for x in GS.inventory:
		print(x.name)




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
	#If no object, print long description of room
	#otherwise print description of item

	#room itself
	if obj == 'e':
		print(GS.current_room.long)
	#----------------------------------------------- Move down to verb_lookat once parser is updated-------------------	
	#items in the room
	for x in GS.item_list:
		if obj == x.name.lower() or obj in x.altnames:
			for y in GS.current_room.items:
				if y == x.name:
					print(x.long)
					if x.featBool:
						print(x.featTrue)
					else:
						print(x.featFalse)
	#features
	if obj in GS.current_room.features:
		print(GS.current_room.features.get(obj))

	#inventory
	for x in GS.inventory:
		if obj == x.name.lower() or obj in x.altnames:
			print(x.long)
			if x.featBool:
				print(x.featTrue)
			else:
				print(x.featFalse)

	#characters
	if GS.current_room.name in charRoom:
		tempName = charRoom.get(GS.current_room.name)
		#print('tempName is ' + tempName)
		for x in GS.char_list:
			if tempName == x.name:
				if obj == x.name.lower() or obj in x.altnames:
					print('Still need to implement character descriptions') #--------------------------------------------------------------------------

	#-------------------------------------------------------------------------------------------------------------------


def verb_lookat(GS, obj):
	pass



def util_verb_take(GS, item):
	for x in GS.item_list:
		if x.name == item.name:
			GS.inventory.append(item)
			GS.current_room.items.remove(item.name)
			print('You are now holding a ' + item.name)
			#add to inventory
			#remove from room inventory


def verb_take(GS, obj):
	#make sure user has a backpack
	#verify item is in the room
	#add item to inventory if possible
	
	#Make sure its in the room
	take = False
	tempItem = None
	for x in GS.current_room.items:						#look at all the names of items in the room
		for y in GS.item_list:						#and all the items in the master item_list
			if x == y.name:						#find the item in item_list that matches the name of the item in the room
				if obj == y.name.lower() or obj in y.altnames:	#if that item is what the user entered
					tempItem = y				#save the item
					take = True				#say we're going to take it

	#Item wasn't found in this room
	if take == False:
		print('Can\'t find that here.')

	else:
		if tempItem.name == 'backpack':
			if GS.backpack == True:
				print('You are already holding that')
			else:
				GS.backpack = True
				util_verb_take(GS, tempItem)
		else:
			if GS.backpack == False:
				print('You need somewhere to put that...')
			else:
				util_verb_take(GS, tempItem)
		


def verb_talk(GS, obj):
	pass

def verb_ask(GS, obj):
	pass

def verb_drop(GS, obj):
	drop = False
	for x in GS.inventory:
		if obj == x.name.lower() or obj in x.altnames:
			if x.name == 'backpack':
				print('That\'s too important to put down!')
				drop = True
			else:
				GS.current_room.items.append(x.name)
				GS.inventory.remove(x)
				drop = True
				print('You are no longer holding a ' + x.name)
	if drop == False:
		print('You\'re not holding that')			



def verb_open(GS, obj):
	pass






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



		if s.verb == 'go' or s.verb == 'move':
			verb_go(GS, s.object)
        
		if s.verb == 'look':
			verb_look(GS, s.object)

		if s.verb == 'lookat':
			verb_lookat(GS, s.object)

		if s.verb == 'take' or s.verb == 'pickup' or s.verb == 'grab':
			verb_take(GS, s.object)

		

		
		if s.verb == 'talk':
			verb_talk(GS, s.object)

		if s.verb == 'ask':
			verb_ask(GS, s.object)

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



