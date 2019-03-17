'''
game.py
The main game file for GloryDaze Text Adventure.
started during engine development, debug and test.
by: Michael Fuelling

CS467
Winter 2019
Team Keid :: Michael Fuelling, Richard Ratliff, Jordan Riojas

Credits:
- https://stackoverflow.com/questions/14796323/input-using-backspace-and-arrow-keys
'''

import time
import sys
import readline
import os

import command
from parser_files import parser
from parser_files import lexicon
import data_format as DF
import util

directions = ["north", "south", "east", "west", "northeast", "southeast", "northwest", "southwest"]

DELAY_LESS = 0.005   # make this smaller for a faster scroll
DELAY = 0.01    # make this smaller for a faster scroll
MAXLEN = 70     # maximum line length to print

class GameState:
	def __init__(self):
		#timing
		self.start = None
		self.elapsed = 0

		self.steps = 0

		#Player
		self.player = None

		#Map
		self.room_list = None
		self.exit_list = None
		self.item_list = None
		self.char_list = None
		self.current_room = None
		self.current_exit = None

		#items
		self.backpack = False
		self.inventory = []

		#characters
		self.talk_count = {
			"coach" : 0,
			"teacher" : 0,
			"counselor" : 0,
			"director" : 0,
			"janitor" : 0,
			"librarian" : 0,
			"principal" : 0
		}

		#Story line specifics
		self.storyFlags = {    
		#rooms
		"Main Office" : 0,
		"Hallway 2" : 0,
		"Supply Room" : 0,
		"Principal Office" : 0,
		"Hallway 3" : 1,

		#items
		"piccolo" : 0,
		"book" : 0,

		"h3c" : 0,
		"h3sd" : 0,

		"sdgive" : 0
		}


		#conditions
		self.win = 0
		self.lose = 0
		self.turnCount = 0

		self.endGame = 0
	

	def print(self):
		print('start - ' + str(self.start))
		print('elapsed - ' + str(self.elapsed))
	
		print('steps - ' + str(self.steps))

		print('player name - ' + self.player.get_name())
	
		#skip room list
		#skip exit list
		#skip item list
		#skip char list
		print('current room - ' + self.current_room.get_name())
		#skip current exit 

		if self.backpack == False:
			print('backpack - ' + 'False')
		else:
			print('backpack - ' + 'True')

		print('Inventory:')
		for x in self.inventory:
			print(x.name)
		print('')

		print ('talk counts:')
		for y in self.talk_count:
			print(y + ' - ' + str(self.talk_count.get(y)))
		print('')

		print ('story flags:')
		for z in self.storyFlags:
			print(z + ' - ' + str(self.storyFlags.get(z)))
		print('')

		print('win - ' + str(self.win))
		print('lose - ' + str(self.lose))
		print('turn count - ' + str(self.turnCount))
		print('end game - ' + str(self.endGame))



def save_game(GS):
	print('Are you sure you want to save?  Any existing save file will be overwritten (y/n)')
	uInput = input('>')
	if uInput.lower() == 'n':
		print('Save Game cancelled')
	elif uInput.lower() == 'y':
		print('saving game....')

		#all in a "save game" directory
		dir = './data/saves/'

		#gamestate - save everything
		f = open(dir + 'gamestate.txt', 'w')

		f.write(str(GS.start))
		f.write('\n')
		f.write(str(GS.elapsed))
		f.write('\n')

		f.write(str(GS.steps))
		f.write('\n')	

		f.write(GS.player.get_name())
		f.write('\n')

		#skip room list
		#skip exit list
		#skip item list
		#skip char list
		f.write(GS.current_room.get_name())
		f.write('\n')
		#skip current exit 

		if GS.backpack == False:
			f.write('F')
			f.write('\n')
		else:
			f.write('T')
			f.write('\n')

		for x in GS.inventory:
			f.write(x.name)
			f.write('\n')

		f.write('ENDINV') # call out end of inventory list because we don't know how long it is
		f.write('\n')

		for y in GS.talk_count:
			f.write(str(y) + ', ' + str(GS.talk_count.get(y)))
			f.write('\n')


		for z in GS.storyFlags:
			f.write(str(z) + ', ' + str(GS.storyFlags.get(z)))
			f.write('\n')

		#skip win
		#skip lose
		f.write(str(GS.turnCount))
		f.write('\n')
		#skip endGame

		#-------------------------------- Data ----------------------------------------------
		# Reminder: dir = './data/saves/'

		#rooms - item list and visited changes
		for x in GS.room_list:
			#print(x.name)
			#print(x.visited)
			#print(x.items)
			util.save(x)

		#items - FeatBool changes
		for x in GS.item_list:
			util.save(x)

		#save chars optional, do not change

		#save exits optional, do not change
	
		#-------------------------------------------------------------------------------------

		#tell user game was successfully saved
		print('Game successfully saved.')
	else:
		print('Please enter y or n')
		save_game(GS)


def load_game():
	print('Are you sure you want to load a game?  Any unsaved progress will be lost (y/n)')
	uInput = input('>')
	if uInput.lower() == 'n':
		print('Load Game cancelled')
		return 'cancel'
	elif uInput.lower() == 'y':
		print('Loading game...')
		#Load everything into gamestate here
		dir = './data/saves/'

		exist = os.path.isfile(dir + 'gamestate.txt')
		if exist == False:
			print('ERROR: Can\'t find saved game files')
			return 'error'
		else:

			#gamestate - Load everything
			LGS = GameState()
			'''
			LGS.start = None
			LGS.elapsed = 0
			LGS.steps = 0
			LGS.player = None
			LGS.room_list = None
			LGS.exit_list = None
			LGS.item_list = None
			LGS.char_list = None
			LGS.current_room = None
			LGS.current_exit = None
			LGS.backpack = False
			LGS.inventory = []
			LGS.talk_count = {
				"coach" : 0,
				"teacher" : 0,
				"counselor" : 0,
				"director" : 0,
				"janitor" : 0,
				"librarian" : 0,
				"principal" : 0
			}
			LGS.storyFlags = {    
			"Main Office" : 0,
			"Hallway 2" : 0,
			"Supply Room" : 0,
			"Principal Office" : 0,
			"Hallway 3" : 1,
			"piccolo" : 0,
			"book" : 0,
			"h3c" : 0,
			"h3sd" : 0,
			"sdgive" : 0
			}
			LGS.win = 0
			LGS.lose = 0
			LGS.turnCount = 0
			LGS.endGame = 0
			'''

			p = DF.Player()	
			LGS.player = p	

			# Gamestate
			f = open(dir + 'gamestate.txt', 'r')
			lines = f.readlines()


			#lineCount = 0
			#for x in lines:
			#	lineCount = lineCount + 1

			
			for x in range(len(lines)):
				lines[x] = lines[x].rstrip()
			#print(lines)
			

			LGS.start = float(lines[0])
			LGS.elapsed = int(lines[1])
			LGS.steps = int(lines[2])
			LGS.player.set_name(lines[3])

			#lines[4] is room name.  Set below after rooms loaded in

			if lines[5] == 'F':
				LGS.backpack = False
			else:
				LGS.backpack = True

			#Items
			idx = 6
			tempItem = 0
			inventoryList = []
			while tempItem != 'ENDINV':
				tempItem = lines[idx]
				inventoryList.append(tempItem)
				idx = idx + 1

			#Talk counts
			tempTalks = []
			for x in range(7):
				tempTalks.append(lines[idx + x])
			#print(tempTalks)

			for x in tempTalks:
				tempS = x.split(', ')
				#print(tempS)
				for y in LGS.talk_count:
					if y == tempS[0]:
						LGS.talk_count[y] = tempS[1]
						#print('set ' + y + ' to ' + tempS[1])


			idx = idx + 7

			#Story flags
			tempFlags = []
			for x in range(10):
				tempFlags.append(lines[idx + x])
			#print(tempFlags)

			for x in tempFlags:
				tempS = x.split(', ')
				#print(tempS)
				for y in LGS.storyFlags:
					if y == tempS[0]:
						LGS.storyFlags[y] = tempS[1]
						#print('set ' + y + ' to ' + tempS[1])

			idx = idx + 10

			LGS.turnCount = int(lines[idx])

			#-------------------------------- Data ----------------------------------------------
			# Reminder: dir = './saves/'

			ROOMS = ["Bathroom","Cafeteria","Chemistry","Computer Lab","Counselor Office","Detention","Gym","Hallway 1","Hallway 2","Hallway 3","Janitor Office","Library","Main Office","Math","Music","Principal Office","Supply Room"]
			#rooms - item list and visited changes
			tRooms = []
			for x in ROOMS:
				#print(x.name)
				tRooms.append((util.load(x)))

			#for x in tRooms:
				#print(x.name)
				#print(x.visited)
				#print(x.items)
			LGS.room_list = tRooms

			
			ITEMS = ["backpack","book","water bottle","calculator","camera","cellphone","duct tape","Office Pass","piccolo","SD card"]
			#items - FeatBool changes			
			tItems = []
			for x in ITEMS:
				tItems.append(util.load(x))
			LGS.item_list = tItems

			#load chars from original
			char_builder = DF.CharacterBuilder()
			LGS.char_list = DF.CharacterBuilder.load_char_files(char_builder)

			#load exits from original	
			exit_builder = DF.ExitBuilder()	
			LGS.exit_list = DF.ExitBuilder.load_exit_files(exit_builder)

			#-------------------------------------------------------------------------------------

			#More gamestate
    		#load current room based on name
			for x in LGS.room_list:
				if x.name == lines[4]:
					LGS.current_room = x

    		#load items into inventory based on name
			for x in inventoryList:
				for y in LGS.item_list:
					if x == y.name:
						LGS.inventory.append(y)


			print('Load Game successful')
			'''
			for x in LGS.room_list:
				print(x.name)
				for y in x.items:
					print('items: ' + y)
			print('Inventory')
			for x in LGS.inventory:
				print(x)
			#print('In load game function:')
			#LGS.print()
			'''
			return LGS

	else:
		print('Please enter y or n')
		x = load_game()
		if x == 'error':
			return 'error'
		elif x == 'cancel':
			return 'cancel'
		else:
			return x



def GameLoop(GS):
	"""
	"Gaming Loop" which loops for user input and attempts to execute it.  
	"""
	#start = time.time() #Moved to before gameloop is called
	uInput = 0
	while uInput != 'q':
		uInput = input('("q" to quit) >')

		s = parser.parse_sentence(lexicon.scan(uInput.lower()))
		# print(s.subject)
		# print(s.verb)
		# print(s.object + '\n')
		print()

		if uInput == 'print':
			GS.print()

		if GS.endGame == 1:
			GS.win = 1;

		elif s.verb == 'save':
			save_game(GS)

		elif s.verb == 'load':
			LGS = load_game()
			if LGS == 'error':
				print('Returning to current game.')
			elif LGS == 'cancel':
				print('Returning to current game.')
			else:
				#print('In game loop:')
				#LGS.print()
				#----------------------------- Start new game with Loaded gamestate -----------------------------
				#Print room description so user knows where they are and start looping for input
				print('-' * 70, '\n\n\n')
				#print('Moved to ' + GS.current_room.get_name())
				util.print_ascii_art('./data/artwk/' + LGS.current_room.get_name())
				print('')
				util.scroll3(0.01, 60, LGS.current_room.get_long())
				print('')
				#print(gamestate.current_room.get_items())
				#print('')
				for item in LGS.current_room.get_items():
					for x in LGS.item_list:
						if x.name == item:
							# print("{}".format(x.get_long()))
							util.scroll3(0.01, 60, "{}".format(x.get_avail()))
				print('')
				#print(gamestate.current_room.get_exits())
				#print('')
				exits = LGS.current_room.get_exits()
				for exits_dir, exits_room in exits.items():
					for x in LGS.exit_list:
						if x.name == exits_room and exits_dir in directions:
							util.scroll3(0.01, 60, "{} {}".format(x.get_long(),exits_dir))
				print('')

				LGS.start = time.time()
				del GS
				GameLoop(LGS)  
				return

		else:
			command.command(GS, s)
	
		if GS.endGame == 1:
			GS.win = 1;
	
		print('')		

		elapsed = int(time.time() - GS.start)
		# print('elapsed time is {:02d}:{:02d}:{:02d}'.format(elapsed // 3600, (elapsed % 3600 // 60), elapsed % 60))
		
		# -------------------- RELEVANT TO GAME.  UNCOMMENT AFTER DEBUG -----------------------------------------
		print('\nelapsed time is {:02d}:{:02d}'.format((elapsed % 3600 // 60), elapsed % 60))
		print('')
		# -------------------------------------------------------------------------------------------------------		

		GS.elapsed = elapsed
		if (GS.elapsed > 1800):
			GS.lose = 1

		# GS.win = 1 # test win condition,  TODO to set it up

		#End of turn maintenance
		GS.turnCount = GS.turnCount + 1
		if GS.win == 1:
			util.print_you_won()
			print('')
			print('Your time was', round(GS.elapsed/60, 1), 'minutes.')
			print('It took you ' + str(GS.turnCount) + ' turns.')
			print('')
			quit()
		elif GS.lose == 1:
			util.print_sorry_you_lost()
			print('')
			print('Your elapsed time was more than 30 minutes.')
			print('You got this far in ' + str(GS.turnCount) + ' turns.')
			print('Load your save game or try again from the start!')
			print('')
			quit()
		
        
		'''
		print('')
		print('End of turn.')
		print('')
		'''

def RunGame(type):
    """
    Setups up the gamestate, rooms, player, objects, and characters depending on if a new game or loaded game.  Once the game is setup, calls GameLoop() with the setup gamestate to loop for user input
    """

    #NEW GAME
    if type == 0:           

        #Setup Gamestate
        gamestate = GameState()

        #Setup player
        p = DF.Player()
        gamestate.player = p

        #setup rooms
        #print('\nBuilding rooms from files')
        room_builder = DF.RoomBuilder()
        gamestate.room_list = DF.RoomBuilder.load_room_files(room_builder)
        exit_builder = DF.ExitBuilder()
        gamestate.exit_list = DF.ExitBuilder.load_exit_files(exit_builder)
        item_builder = DF.ItemBuilder()
        gamestate.item_list = DF.ItemBuilder.load_item_files(item_builder)
        char_builder = DF.CharacterBuilder()
        gamestate.char_list = DF.CharacterBuilder.load_char_files(char_builder)
	

        #print('\nChecking rooms loaded into gamestate:')
        #for x in gamestate.room_list:
            #print(x.name)

        #Start in detention
        for x in gamestate.room_list:
            if x.name == 'Detention':
                gamestate.current_room = x
                gamestate.current_room.visited = True
        #print('\nCurrent room is: ' + gamestate.current_room.name)

        
        #Play opener to get player name
        #print('\nNEW GAME OPENER:\n')
        delay = 1.5
        
        opener1 = '"Hey."\n'
        opener2 = '"Hey..."\n'
        opener3 = '"HEY!!!!"\n'

        for letter in opener1:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(0.05)
        #print()
        time.sleep(delay)
            
        for letter in opener2:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(0.05)
        #print()
        time.sleep(delay)
            
        for letter in opener3:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(0.05)
        #print()
        time.sleep(delay)

        print('Hmm.... Uh, what? Where am I?')
        time.sleep(delay + 1)
        
        print('"Where do you think?  You\'re in detention kid.  What\'s your name anyway?"')
        time.sleep(delay + 1)
        
        print('My... My name?  Its....')
        name = input('>')
        gamestate.player.set_name(name)
        time.sleep(delay)
        
        print('"Well, ' + gamestate.player.get_name() + ', it\'s 6:30 PM."')
        time.sleep(delay)
        print('"Detention ended a half hour ago.  Time to go home."')
        time.sleep(delay + 1)
        
        print('What? Its 6:30!? My parents are gonna kill me!')
        time.sleep(delay + 1)

        print('"You better be out of here in 30 minutes or you\'ll be stuck here forever!!!"') 
        print('"Mwahahaha....."')
        time.sleep(delay + 1)

        print('What happens in 30 minutes? And who is talking???')
        time.sleep(delay + 1)

        print('I don\'t like this at all. I better get a move on.')
        time.sleep(delay + 2)
        print('')



    #LOAD GAME
    elif type == 1:    
        gamestate = load_game()
        if gamestate == 'cancel':
        	return 'cancel'    
        elif gamestate == 'error':
        	return 'error'
    
    #Print room description so user knows where they are and start looping for input
    # print('-' * 70, '\n\n\n')
	#print('Moved to ' + GS.current_room.get_name())
    util.print_ascii_art('./data/artwk/' + gamestate.current_room.get_name())
    print('')
    util.scroll3(DELAY, MAXLEN, gamestate.current_room.get_long())
    print('')
    #print(gamestate.current_room.get_items())
    #print('')
    for item in gamestate.current_room.get_items():
        for x in gamestate.item_list:
            if x.name == item:
                # print("{}".format(x.get_long()))
                util.scroll3(DELAY, MAXLEN, "{}".format(x.get_avail()))
    print('')
    #print(gamestate.current_room.get_exits())
    #print('')
    exits = gamestate.current_room.get_exits()
    for exits_dir, exits_room in exits.items():
        for x in gamestate.exit_list:
            if x.name == exits_room and exits_dir in directions:
                util.scroll3(DELAY, MAXLEN, "{} {}".format(x.get_long(),exits_dir))
    print('')

    gamestate.start = time.time()
    GameLoop(gamestate)  

    

def Title():
    """
    First functions called to play the game.
    Check terminal size and present title screen for the user.
    Calls MainMenu() and game loops to MainMenu(), not here, for some choices.
    """
    util.term_check()
    util.print_title()
    MainMenu()


def MainMenu():
    """
    Calls RunGame() once the user chooses new game or load game.
    """
    util.print_start_menu() # uses menu in ./data/artwk/start_menu
    
    selection = input('>')

    selections = ['1', '2', '3', '4', '5']
    if selection not in selections:
        print('Please input a valid integer 1, 2, 3, or 4')
        print('')
        MainMenu()
    else:
        if selection == '1':
            print('Starting NEW GAME')
            RunGame(0)      

        elif selection == '2':
            #RunGame(1)
            print('LOADING GAME from save file.\n')
            x = RunGame(1)
            if x == 'cancel':
                MainMenu()
            elif x == 'error':
                MainMenu()

        elif selection == '3':
            util.scroll3(DELAY_LESS, MAXLEN, 'GloryDaze is a text only adventure.  '+
            'That means there are no graphics! Everything about the game '+
            'will be displayed on the screen. Want to do something? Just '+
            'type it in!')
            print('')
            util.scroll3(DELAY_LESS, MAXLEN, '(a ">" symbol means the game is waiting for your '+
            'input)')
            print('')
            util.scroll3(DELAY_LESS, MAXLEN, 'The game allows for as much natural language as possible '+
            'but if you\'re having trouble getting around, try shorter sentences '+
            'like "move south" or "take book".')
            print('')
            util.scroll3(DELAY_LESS, MAXLEN, 'At any '+
            'point during the game, type "save" to save your progress '+
            'or "help" for help.')
            print('')
            util.scroll3(DELAY_LESS, MAXLEN, 'Finally, your terminal may allow you to scroll up '+
            'to see your past actions which may help you. :)')
            print('')
            print('Have fun!')
            print('')
            MainMenu()

        elif selection == '4':
            print('Have a nice day!')
            quit()

        elif selection == '5':
            #Setup Gamestate
            gamestate = GameState()

            #Setup player
            p = DF.Player()
            gamestate.player = p

            #setup room
            print('\nBuilding rooms from files')
            room_builder = DF.RoomBuilder()
            gamestate.room_list = DF.RoomBuilder.load_room_files(room_builder)
            exit_builder = DF.ExitBuilder()
            gamestate.exit_list = DF.ExitBuilder.load_exit_files(exit_builder)
            item_builder = DF.ItemBuilder()
            gamestate.item_list = DF.ItemBuilder.load_item_files(item_builder)
            char_builder = DF.CharacterBuilder()
            gamestate.char_list = DF.CharacterBuilder.load_char_files(char_builder)
	
            #print('\nChecking rooms loaded into gamestate:')
            #for x in gamestate.room_list:
            #print(x.name)

            #Start in detention
            for x in gamestate.room_list:
                if x.name == 'Detention':
                    gamestate.current_room = x
                    gamestate.current_room.visited = True
            print('\nCurrent room is: ' + gamestate.current_room.name)
            gamestate.player.set_name('TEST')
            gamestate.start = time.time()

            GameLoop(gamestate)



# Title, which calls MainMenu, instead of MainMenu here allows
# terminal size check one time only and printing of GloryDaze
# one time especially when option 3 help is used in a minimum
# size terminal - GloryDaze art scrolls part of help off screen
# MainMenu()

Title()

