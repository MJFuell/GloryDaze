'''
game.py
The main game file for GloryDaze Text Adventure.
started during engine development, debug and test.
by: Michael Fuelling

CS467
Winter 2019
Team Keld :: Michael Fuelling, Richard Ratliff, Jordan Riojas

Credits:
- https://stackoverflow.com/questions/14796323/input-using-backspace-and-arrow-keys
'''

import time
import sys
import readline

import command
from parser_files import parser
from parser_files import lexicon
import data_format as DF
import util

directions = ["north", "south", "east", "west", "northeast", "southeast", "northwest", "southwest"]



class GameState:
	#timing
	start = None
	elapsed = None

	steps = 0

	#Player
	player = None

	#Map
	room_list = None
	exit_list = None
	item_list = None
	char_list = None
	current_room = None
	current_exit = None

	#items
	backpack = False
	inventory = []

	#characters
	talk_count = {
		"coach" : 0,
		"teacher" : 0,
		"counselor" : 0,
		"director" : 0,
		"janitor" : 0,
		"librarian" : 0,
		"principal" : 0
	}

	#Story line specifics
	storyFlags = {    
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
	win = 0
	lose = 0
	turnCount = 0

	endGame = 0

	#Initializer
	def __init__(self):
		pass



def save_game(GS):
	print('SAVE GAME - not implemented yet')
	#Save everything into files here--------------------------------------------------------------------------------------------
	#all in a "save game" directory

	#gamestate - save everything

	#rooms - only item list changes

	#items - only FeatBool changes

	#don't need to save chars or exits as they don't change
	

	#tell user game was successfully saved


def load_game():
	print('LOAD GAME - not implemented yet')
    #Load everything into gamestate here -------------------------------------------------------------------------------------------

    #gamestate - Load everything

    #rooms - only change is what items are in there

    #items - only change is FeatBool True/False

    #don't need to load chars or exits as they don't change

	
	#return loaded gamestate




def GameLoop(GS):
	"""
	"Gaming Loop" which loops for user input and attempts to execute it.  
	"""
	#start = time.time() #Moved to before gameloop is called
	uInput = 0
	while uInput != 'q':
		uInput = input('("q" to quit) >')

		s = parser.parse_sentence(lexicon.scan(uInput.lower()))
		print(s.subject)
		print(s.verb)
		print(s.object + '\n')

		if GS.endGame == 1:
			GS.win = 1;

		elif s.verb == 'save':
			save_game(GS)

		elif s.verb == 'load':
			load_game()

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
		if (GS.elapsed > 1200):
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
			print('Your elapsed time was more than 20 minutes.')
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

        print('"You better be out of here in 20 minutes or you\'ll be stuck here forever!!! Muahahaha....."')
        time.sleep(delay + 1)

        print('What happens in 20 minutes? And who is talking???')
        time.sleep(delay + 1)

        print('I don\'t like this at all. I better get a move on.')
        time.sleep(delay + 2)
        print('')



    #LOAD GAME
    if type == 1:    
        gamestate = load_game()      

    
    #Print room description so user knows where they are and start looping for input
    print('-' * 70, '\n\n\n')
	#print('Moved to ' + GS.current_room.get_name())
    util.print_ascii_art('./data/artwk/' + gamestate.current_room.get_name())
    print('')
    util.scroll3(0.01, 60, gamestate.current_room.get_long())
    print('')
    #print(gamestate.current_room.get_items())
    #print('')
    for item in gamestate.current_room.get_items():
        for x in gamestate.item_list:
            if x.name == item:
                # print("{}".format(x.get_long()))
                util.scroll3(0.01, 60, "{}".format(x.get_avail()))
    print('')
    #print(gamestate.current_room.get_exits())
    #print('')
    exits = gamestate.current_room.get_exits()
    for exits_dir, exits_room in exits.items():
        for x in gamestate.exit_list:
            if x.name == exits_room and exits_dir in directions:
                util.scroll3(0.01, 60, "{} {}".format(x.get_long(),exits_dir))
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
            print('LOAD GAME not yet implemented.\n')
            MainMenu()

        elif selection == '3':
            util.scroll3(0.005, 60, 'GloryDaze is a text only adventure.  '+
            'That means there are no graphics! Everything about the game '+
            'will be displayed on the screen. Want to do something? Just '+
            'type it in!')
            util.scroll3(0.005, 60, '(a ">" symbol means the game is waiting for your '+
            'input)')
            print('')
            util.scroll3(0.005, 60, 'The game allows for as much natural language as possible '+
            'but if you\'re having trouble getting around, try shorter sentences '+
            'like "move south" or "take book".')
            print('')
            util.scroll3(0.005, 60, 'At any '+
            'point during the game, type "save" to save your progress '+
            'or "help" for help.')
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

