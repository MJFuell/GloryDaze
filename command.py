'''
command.py
command processor of the game engine.
by: Michael Fuelling

CS467
Winter 2019
Team Keid :: Michael Fuelling, Richard Ratliff, Jordan Riojas
'''

import util

DELAY = 0.01    # make this smaller for a faster scroll
MAXLEN = 70     # maximum line length to print


directions = ["north", "south", "east", "west", "northeast", "southeast", "northwest", "southwest"]
charRoom = {
    "Gym" : "coach",
    "Computer Lab" : "teacher",
    "Counselor Office" : "counselor",
    "Music" : "director",
    "Janitor Office" : "janitor",
    "Library" : "librarian",
    "Principal Office" : "principal"
}


#text for failing story line specifics
storyFlagText = {
    #rooms
    "Main Office" : "That room is locked.  It seems it could be unlocked remotely.",
    "Hallway 2" : "You notice a cart full of books in the way.\nLibrarian: 'I'll move those books in a little bit!  Why don't you go talk to other teachers in the mean time.",
    "Supply Room" : "Janitor: 'Hey kid! Don't you dare go in there without talking to me first!!!'",
    "Principal Office" :"That room is locked.",
    "Hallway 3" : "You should probably wash your hands first...",

    #items
    "piccolo" : "Director: 'Don't go messing around with my instruments! Maybe once i'm done with this you can take one.'",
    "book" : "Librarian: 'I'm in no mood to let you take my stuff!!'",
}


dodge = ['dodge', 'duck', 'dip', 'dive']

err = "Can't do that"



def end_game(GS):
	util.scroll3(DELAY, MAXLEN, 'Principal: "Well, well, well.  So you finally found me."')
	util.scroll3(DELAY, MAXLEN, 'Principal: "Let me guess, you\'ve been running around the school unsupervised, talking to teachers and stealing things?!?"')
	util.scroll3(DELAY, MAXLEN, 'Principal: "Give me that backpack!"')
	util.scroll3(DELAY, MAXLEN, 'The principal takes your backpack and begins rummaging through your stuff.')
	sd = False
	cam = False
	for x in GS.inventory:
		if x.name == 'camera':
			cam = True
		elif x.name == 'SD card':
			sd = True
	if cam == False:
		util.scroll3(DELAY, MAXLEN, 'Principal: "Hmmm you didn\'t find my camera anywhere?  Hang on, let me go grab it real quick."')
		util.scroll3(DELAY, MAXLEN, 'The principal returns after 2 minutes.')		
		GS.start = GS.start - 120
	else:
		util.scroll3(DELAY, MAXLEN, 'Principal: "Thanks for finding my camera!"')

	util.scroll3(DELAY, MAXLEN, 'Principal: "Okay, what else do we have here..."')

	if sd == False:
		util.scroll3(DELAY, MAXLEN, 'Principal: "Darn you don\'t have my SD card?  I\'ll be right back."')
		if GS.storyFlags['sdgive'] == 0:
			util.scroll3(DELAY, MAXLEN, 'The principal returns after 3 minutes.')
			util.scroll3(DELAY, MAXLEN, 'Principal: "Found it!  All good.  Let\'s get you home, ' + GS.player.get_name() + '!"')
			GS.start = GS.start - 180
		else:
			util.scroll3(DELAY, MAXLEN, 'The principal returns after 5 minutes.')
			util.scroll3(DELAY, MAXLEN, 'Principal: "You gave my SD card to the TEACHER IN THE COMPUTER LAB?!?"')
			util.scroll3(DELAY, MAXLEN, 'Principal: "DO YOU HAVE ANY IDEA WHAT WAS ON THERE!!!!"')
			util.scroll3(DELAY, MAXLEN, 'Principal: "Well, if you do you better keep your mouth shut about it."')
			util.scroll3(DELAY, MAXLEN, 'Principal: "Or else you\'ll have detention for a year!"')
			util.scroll3(DELAY, MAXLEN, 'Principal: "Alright, time to get you out of here, ' + GS.player.get_name() + '."')
			GS.start = GS.start - 300
	else:
		util.scroll3(DELAY, MAXLEN, 'Principal: "Oh my SD card! Thank goodness that didn\'t fall into the wrong hands...."')
		util.scroll3(DELAY, MAXLEN, 'Principal: "Alright, let\'s get you out of here, ' + GS.player.get_name() + '."')

	util.scroll3(DELAY, MAXLEN, 'The principal walks you out of his office and out the main exit of the school!')

	GS.endGame = 1




def verb_help(GS, obj):
	print('           ------------ HELP SCREEN ------------')
	print('The goal is to escape school before you run out of time.')
	print('In order to do that you\'ll need to interact with items and people.')
	print('Here\'s a few verbs to help you get around:')
	print('')
	print('save        - save your current progress (only one save file exists at a time)')
	print('load        - end your current game and load from a saved file')
	print('help        - print this help screen')
	print('')
	print('inventory   - view the items currently in your inventory')
	print('items       - view the items currently in your current room')
	print('exits       - view the exits from your current room')	
	print('people      - view the people in your current room')
	print('look        - view a description of the current room')
	print('')
	print('look at ___ - view a description of a particular thing')
	print('go ___      - move a particular direction or to a particular room')
	print('take ___    - add an item to your inventory')
	print('drop ___    - leave something from your inventory in the current room')
	print('talk ___    - talk to someone')
	print('ask ___     - ask someone for help')
	print('give ___    - give something to whoever is in the room')
	print('use ___     - use an item you are holding or in the room')
	

	

def verb_inventory(GS, obj):
	#display current inventory
	empty = True
	print('You are currently holding:')
	for x in GS.inventory:
		empty = False
		print(x.name)

	if empty:
		print('Nothing')


def verb_exits(GS, obj):
	for x in GS.current_room.exits:
		if x in directions:
			print(x + " : " + GS.current_room.exits.get(x))

	#for val in set(GS.current_room.get_exits().values()):
	#	print(val)


def verb_items(GS, obj):
	empty = True
	for x in GS.current_room.items:
		for y in GS.item_list:
			if x == y.name:
				empty = False
				print(y.name)
	if empty:
		print('No items here')


def verb_people(GS, obj):
	if GS.current_room.name in charRoom:
		print(charRoom.get(GS.current_room.name))
		
	else:
		print('No people here')


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



def verb_go(GS, obj):
	move = False
	tempRoom = None

	#Room name or alt room name
	#Make sure that room is adjacent
	for x in GS.room_list:
		#print('x.name = ' + x.name)
		#print('x.altnames = ' + ", ".join(str(e) for e in x.altnames))
		if obj == x.name.lower() or obj in x.altnames:
			#print('x is ' + x.name)
			if x.name in GS.current_room.exits.values():
				tempRoom = x
				move = True

			
	#Directions
	#Make sure you can travel that direction from current room
	if obj in GS.current_room.exits:
		roomName = GS.current_room.exits.get(obj)
		for x in GS.room_list:
			if x.name == roomName:
				tempRoom = x
				move = True

	#if story line prevents us from being able to move there
	if move == True:
		if tempRoom.name in GS.storyFlags:
			if GS.storyFlags.get(tempRoom.name) == 0:
				util.scroll3(DELAY, MAXLEN, storyFlagText.get(tempRoom.name))
				move = False

	#If we successfully moved rooms
	if move == True:
		GS.current_room = tempRoom
		# print('-' * 70, '\n\n\n')
		exits = GS.current_room.get_exits()
		#print('Moved to ' + GS.current_room.get_name())
		util.print_ascii_art('./data/artwk/' + GS.current_room.get_name())
		print('')
		if GS.current_room.visited:
			util.scroll3(DELAY, MAXLEN, GS.current_room.get_short())
			print('')
			for item in GS.current_room.get_items():
				for x in GS.item_list:
					if x.name == item or item in x.altnames:
						util.scroll3(DELAY, MAXLEN, "{}".format(x.get_avail()))
						print('')
			for exits_dir, exits_room in exits.items():
				for x in GS.exit_list:
					if x.name == exits_room and exits_dir in directions:
						util.scroll3(DELAY, MAXLEN, "{} {}".format(x.get_short(),exits_dir))
						print('')
		else:
			util.scroll3(DELAY, MAXLEN, GS.current_room.get_long())
			print('')
			for item in GS.current_room.get_items():
				for x in GS.item_list:
					if x.name == item or item in x.altnames:
						util.scroll3(DELAY, MAXLEN, "{}".format(x.get_avail()))
						print('')
			for exits_dir, exits_room in exits.items():
				for x in GS.exit_list:
					if x.name == exits_room and exits_dir in directions:
						util.scroll3(DELAY, MAXLEN, "{} {}".format(x.get_long(),exits_dir))
						print('')
		GS.current_room.visited = True

		#--------------------------------------------------------
		#Items falling out
		for x in GS.inventory:
			if x.name == 'backpack':
				if x.featBool == 'False':
					if GS.steps == 5:
						pass
						#drop a random item
						#give user a hint about an item falling out
						#reset step count
					else:
						GS.steps = GS.steps + 1


		#--------------------------------------------------------

	#If we did not move
	else:
		print('Can\'t go that way')
        

def verb_look(GS, obj):
	#If no object, print long description of room
	util.scroll3(DELAY, MAXLEN, GS.current_room.long)



def verb_lookat(GS, obj):
	#items in the room
	look = False
	for x in GS.item_list:
		if obj == x.name.lower() or obj in x.altnames:
			look = True
			for y in GS.current_room.items:
				if y == x.name:
					util.scroll3(DELAY, MAXLEN, x.long)
					if x.featBool == True:
						util.scroll3(DELAY, MAXLEN, x.featTrue)
					else:
						util.scroll3(DELAY, MAXLEN, x.featFalse)
	#features
	if obj in GS.current_room.features:
		look = True
		util.scroll3(DELAY, MAXLEN, GS.current_room.features.get(obj))

	#inventory
	for x in GS.inventory:
		if obj == x.name.lower() or obj in x.altnames:
			look = True
			util.scroll3(DELAY, MAXLEN, x.long)
			if x.featBool == 'True':
				util.scroll3(DELAY, MAXLEN, x.featTrue)
			else:
				util.scroll3(DELAY, MAXLEN, x.featFalse)

	#characters
	if GS.current_room.name in charRoom:
		tempName = charRoom.get(GS.current_room.name)
		if obj == tempName:
			look = True
		#print('tempName is ' + tempName)
			for x in GS.char_list:
				if tempName == x.name:
					util.scroll3(DELAY, MAXLEN, x.desc)

	if look == False:
		print('Can\'t see that')


def util_verb_take(GS, item):
	for x in GS.item_list:
		if x.name == item.name:
			GS.inventory.append(item)
			GS.current_room.items.remove(item.name)
			print('You are now holding a ' + item.name)
			if item.name == 'SD card':
				GS.storyFlags['h3sd'] = 1
				if GS.storyFlags['h3c'] == 1:
					GS.storyFlags['Hallway 2'] = 1
					GS.talk_count['librarian'] = 1
			#add to inventory
			#remove from room inventory


def verb_take(GS, obj):
	#make sure user has a backpack
	#verify item is in the room
	#add item to inventory if possible
	
	#Make sure its in the room
	take = False
	sl = False
	tempItem = None
	for x in GS.current_room.items:						#look at all the names of items in the room
		for y in GS.item_list:						#and all the items in the master item_list
			if x == y.name:						#find the item in item_list that matches the name of the item in the room
				if obj == y.name.lower() or obj in y.altnames:	#if that item is what the user entered
					tempItem = y				#save the item
					take = True				#say we're going to take it


	if take == True:
		if tempItem.name in GS.storyFlags:
			if GS.storyFlags.get(tempItem.name) == 0:
				util.scroll3(DELAY, MAXLEN, storyFlagText.get(tempItem.name))
				sl = True

	#if no storyline interuption
	if sl == False:
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
	if GS.current_room.name in charRoom:
		tempName = charRoom.get(GS.current_room.name)
		#print('tempName is ' + tempName)
		for x in GS.char_list:
			if obj == x.name:
				if x.name == 'librarian':
					if GS.talk_count.get(x.name) == 0:
						util.scroll3(DELAY, MAXLEN, x.long)
					elif GS.talk_count.get(x.name) == 1:
						util.scroll3(DELAY, MAXLEN, x.short)
					else:
						util.scroll3(DELAY, MAXLEN, x.hint)

				elif x.name == 'counselor':
					if GS.talk_count.get(x.name) == 0:
						util.scroll3(DELAY, MAXLEN, x.long)
						GS.talk_count[x.name] = 1
					elif GS.talk_count[x.name] == 1:
						util.scroll3(DELAY, MAXLEN, x.short)
					else:
						util.scroll3(DELAY, MAXLEN, x.hint)

				elif x.name == 'principal':
					end_game(GS)

				else:
					if x.name == 'janitor':
						GS.storyFlags['Supply Room'] = 1
					if GS.talk_count.get(x.name) == 0:
						util.scroll3(DELAY, MAXLEN, x.long)
						GS.talk_count[x.name] = 1
					else:
						util.scroll3(DELAY, MAXLEN, x.short)
	
	else:
		print('That person isn\'t in this room')


def verb_ask(GS, obj):
	if GS.current_room.name in charRoom:
		tempName = charRoom.get(GS.current_room.name)
		#print('tempName is ' + tempName)
		for x in GS.char_list:
			if obj == x.name:
				if x.name == 'librarian':
					if GS.talk_count.get(x.name) == 0:
						util.scroll3(DELAY, MAXLEN, x.long)
					elif GS.talk_count.get(x.name) == 1:
						util.scroll3(DELAY, MAXLEN, x.short)
					else:
						util.scroll3(DELAY, MAXLEN, x.hint)
				
				elif x.name == 'counselor':
					if GS.talk_count.get(x.name) == 0:
						util.scroll3(DELAY, MAXLEN, x.long)
						GS.talk_count[x.name] = 1
					elif GS.talk_count[x.name] == 1:
						util.scroll3(DELAY, MAXLEN, x.short)
					else:
						util.scroll3(DELAY, MAXLEN, x.hint)


				elif x.name == 'principal':
					end_game(GS)

				else:
					util.scroll3(DELAY, MAXLEN, x.hint)
	else:
		print('That person isn\'t in this room')





def dodgeball(GS):
	print('The varisty dodgeball team hurls balls at you.')
	print('What do you do to avoid them?!?')
	uInput = input('>')
	if uInput.lower() in dodge:
		print('Coach: "Great job, ' + GS.player.get_name() + '. You made me proud.  Go ahead and get outta here."')
	else:
		print('Multiple dodgeballs strike you in the face, liver, kidneys, and spleen. You are knocked unconscious for 3 minutes.')
		print('Coach: "Woah kid are you alright? You really need to watch the movie Dodgeball."')
		print('Coach: "Get outta here before you hurt yourself again, ' + GS.player.get_name() + '!"')
		GS.start = GS.start - 180


def verb_give(GS, obj):
	#print('in give function')
	#print('GS.current_room is ' + GS.current_room.name)
	give = False
	holding = False
	if GS.current_room.name in charRoom:
		#print('current room is in charRoom')
		for x in GS.inventory:
			if obj == x.name.lower() or obj in x.altnames:
				holding = True
				#print('You are holding that and there is someone to give it too')
				if GS.current_room.name == 'Gym':
					for x in GS.inventory:
						if x.name == "water bottle":
							tempItem = x
							if obj == x.name.lower() or obj in x.altnames:
								for y in GS.inventory:
									if y.name == "water bottle":
										GS.inventory.remove(y)
								print('You give your water bottle to the coach.')
								print('Coach: "Thanks! I really needed that. Now that I\'m feeling better... DODGEBALL"')
								GS.storyFlags['h3c'] = 1
								give = True
								if GS.storyFlags['h3sd'] == 1:
									GS.storyFlags['Hallway 2'] = 1
									GS.talk_count['librarian'] = 1
								dodgeball(GS)
				elif GS.current_room.name == "Music":
					for x in GS.inventory:
						if x.name == "calculator":
							tempItem = x
							if obj == x.name.lower() or obj in x.altnames:
								for y in GS.inventory:
									if y.name == "calculator":
										GS.inventory.remove(y)
								print('You give your calculator to the director.')
								print('Director: "Wow thanks so much! This will help a bunch."')
								print('Director: "Please take that piccolo if you want to bang out some sick tunes"')
								GS.storyFlags['piccolo'] = 1
								give = True
				elif GS.current_room.name == "Library":
					for x in GS.inventory:
						if x.name == "piccolo":
							tempItem = x
							if obj == x.name.lower() or obj in x.altnames:
								for y in GS.inventory:
									if y.name == "piccolo":
										GS.inventory.remove(y)
								print('You give your piccolo to the librarian.')
								print('Librarian: "OOOoooOOooooo for ME?! Thank you so much!!!"')
								print('Librarian: "Sorry if I was rude to you before. Take all the books you like!"')
								GS.storyFlags['book'] = 1
								GS.talk_count['librarian'] = 2
								give = True
				elif GS.current_room.name == "Counselor Office":
					for x in GS.inventory:
						if x.name == "cellphone":
							tempItem = x
							if obj == x.name.lower() or obj in x.altnames:
								for y in GS.inventory:
									if y.name == "cellphone":
										GS.inventory.remove(y)
								print('You give your cellphone to the counselor.')
								print('Counselor: "Wow thank you for finding that! I\'ve been looking everywhere."')
								util.scroll3(DELAY, MAXLEN, 'Counselor: "I just remotely unlocked the principal\'s office.  Go see him and he\'ll help you get out."')
								GS.storyFlags['Principal Office'] = 1
								GS.talk_count["counselor"] = 2
								give = True
				elif GS.current_room.name == "Computer Lab":
					for x in GS.inventory:
						if x.name == "SD card":
							tempItem = x
							if obj == x.name.lower() or obj in x.altnames:
								for y in GS.inventory:
									if y.name == "SD card":
										GS.inventory.remove(y)
								print('You give your SD Card to the teacher.')
								print('Teacher: "Wow. Nice find kid. You didn\'t look at what was on there did you?!?"')
								print('Teacher: "Well anyway, thank you. Now get lost!"')
								GS.storyFlags['sdgive'] = 1
								give = True
				else:
					print('No one here wants that')

	else:
		print('There\'s no one here to give that too')	
		holding = True
	
	if holding == False:
		print('You\'re not holding that')	



def verb_use(GS, obj):
	#print('USE: need to implement more items to hold and things in the room')
	have = False

	#Things you're holding
	for x in GS.inventory:
		if x.name == obj or obj in x.altnames:
			if x.name == 'book':
				util.scroll3(DELAY, MAXLEN, 'When you open the book you notice a key fob is inside. You press it and hear a door unlock somewhere.')
				GS.storyFlags["Main Office"] = 1
				have = True

			elif x.name == 'duct tape':
				have = True
				print('You use the duct tape to repair the hole in your backpack.')
				for y in GS.inventory:
					if y.name == 'backpack':
						y.featBool = "True"
				for y in GS.item_list:
					if y.name == 'backpack':
						y.featBool = "True"

			elif x.name == 'camera':
				have = True
				print('You turn on the camera but it says there is no SD card')

			
			elif x.name == 'SD card':
				have = True
				cam = False
				for y in GS.inventory:
					if y.name == 'camera':
						util.scroll3(DELAY, MAXLEN, 'You load the SD card into the camera and find rather scandalous photos of a man wearing nothing but holding a mug that says "World\'s best principal"')
						cam = True
				if cam == False:
					print('You have nothing to view that with')
			
			else:
				print('There\'s nothing you can do with that right now')

	if have == False:
		for y in GS.current_room.features:
			if obj == y:
				if obj == 'toilet' or obj == 'stall' or obj == 'stalls':
					print('You calmly relieve yourself in the cleanest stall you can find.')
					GS.storyFlags['Hallway 3'] = 0;
					have = True

				if obj == 'sink' or obj == 'soap':
					print('You wash your hands.  Although this water almost makes them feel dirtier...')
					GS.storyFlags['Hallway 3'] = 1;
					have = True
	if have == False:
		print('You can\'t use that')


def verb_debug(GS, obj):
	for x in GS.room_list:
		if obj == x.name or obj in x.altnames:
			GS.current_room = x	

def verb_eat(GS, obj):
	for x in GS.inventory:
		if x.name == obj or obj in x.altnames:
			pass #------------------------------------------------------------------------------


def verb_drink(GS, obj):
	for x in GS.inventory:
		if x.name == obj or obj in x.altnames:
			pass #-------------------------------------------------------------------------------


def command(GS, s):
	if s.subject == 'player':

		if s.verb == 'help':
			verb_help(GS, s.object)

		if s.verb == 'inventory':
			verb_inventory(GS, s.object)



		if s.verb == 'exits':
			verb_exits(GS, s.object)

		if s.verb == 'items':
			verb_items(GS, s.object)

		if s.verb == 'people':
			verb_people(GS, s.object)		



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

		if s.verb == 'give':
			verb_give(GS, s.object)	

		if s.verb == 'use':
			verb_use(GS, s.object)	

		if s.verb == 'debug':
			verb_debug(GS, s.object)


		#extras/text only
		if s.verb == 'eat':
			verb_eat(GS, s.object)

		if s.verb == 'drink':
			verb_drink(GS, s.object)




	#movement without verb
	elif s.verb == 'e':
		moved = False
		#room name
		for x in GS.room_list:
			if s.subject == x.name or s.subject in x.altnames:
				moved = True
				verb_go(GS, s.subject)

		#direction
		if s.object in GS.current_room.exits:
			roomName = GS.current_room.exits.get(s.object)
			for x in GS.room_list:
				if x.name == roomName:
					moved = True
					verb_go(GS, s.object)


		if moved == False:
			print('I Don\'t understand')
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



