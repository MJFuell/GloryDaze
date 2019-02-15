

import time
import sys

import data_format as DF
import util

class GameState:
	#Player
	player = 0

	#Map
	room_list = None
	exit_list = None
	item_list = None
	current_room = None
	current_exit = None

	#conditions
	win = 0
	lose = 0
	turnCount = 0

	#Initializer
	def __init__(self):
		pass


def GameLoop(GS):
	"""
	"Gaming Loop" which loops for user input and attempts to execute it.  
	"""
	uInput = 0
	while uInput != 'q':
		uInput = input('("q" to quit, "view" for adjacent rooms, "ROOM_NAME" to move there) >')


        	# ---------------------------------------------------------------------------------------------------------------------------------------
        	#PASS INPUT TO COMMAND PARSE FUNCTION/TRY TO DO WHAT IT SAYS
		for x in GS.room_list:
			if uInput == x.name or uInput in x.altnames:
				GS.current_room = x
				print('-' * 70, '\n\n\n')
				print('Moved to ' + GS.current_room.get_name())
				print('')
				exits = GS.current_room.get_exits()
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
							if x.name == exits_room:
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
							if x.name == exits_room:
								util.scroll3(0.01, 60, "{} {}".format(x.get_long(),exits_dir))
								print('')
				GS.current_room.visited = True

		if uInput == 'view':
			print('')
			util.scroll3(0.01, 60, GS.current_room.get_exits())
	
            
        	# ---------------------------------------------------------------------------------------------------------------------------------------

		#End of turn maintenance
		if GS.win == 1:
			pass
		elif GS.lose == 1:
			pass
		GS.turnCount += GS.turnCount
        
		print('')
		print('End of turn.')
		print('')


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
        print('\nBuilding rooms from files')
        room_builder = DF.RoomBuilder()
        gamestate.room_list = DF.RoomBuilder.load_room_files(room_builder)
        exit_builder = DF.ExitBuilder()
        gamestate.exit_list = DF.ExitBuilder.load_exit_files(exit_builder)
        item_builder = DF.ItemBuilder()
        gamestate.item_list = DF.ItemBuilder.load_item_files(item_builder)

        #print('\nChecking rooms loaded into gamestate:')
        #for x in gamestate.room_list:
            #print(x.name)

        #Start in detention
        for x in gamestate.room_list:
            if x.name == 'Detention':
                gamestate.current_room = x
                gamestate.current_room.visited = True
        print('\nCurrent room is: ' + gamestate.current_room.name)

        
        #Play opener to get player name
        print('\nNEW GAME OPENER:\n')
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
        
        print('"Where the hell do you think? You\'re in detention kid.  What\'s your name anyway?"')
        time.sleep(delay + 1)
        
        print('My... My name?  Its....')
        name = input('>')
        gamestate.player.set_name(name)
        time.sleep(delay)
        
        print('"Well, ' + gamestate.player.get_name() + ', it\'s 6:30 PM.  Detention ended a half hour ago.  Time to go home."')
        time.sleep(delay + .5)
        
        print('What? Its 6:30!? Crap! My parents are gonna kill me. I better get out of here!\n')
        time.sleep(delay)



    #LOAD GAME
    if type == 1:           
        #Load from save file
        pass

    
    #Print room description so user knows where they are and start looping for input
    print('You are in ' + gamestate.current_room.get_name())
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
            if x.name == exits_room:
                util.scroll3(0.01, 60, "{} {}".format(x.get_long(),exits_dir))
    print('')

    GameLoop(gamestate)  

    



def MainMenu():
    """
    First function called to play the game.  Presents the title screen to the user.  Calls RunGame() once the user chooses new game or load game
    """
    util.print_title()

    util.scroll3(0.01, 60, 'Welcome to GloryDaze! The world\'s finest '+
    'text-only school escape adventure. Please enter the number of an '+
    'option below. (Free typing is allowed once the game starts)\n')
    print('1. New Game')
    print('2. Load Game')
    print('3. How to Play')
    print('4. Quit')

    try:
        selection = int(input('>'))
    except ValueError:
        print('Please input a valid integer 1, 2, 3, or 4')
        MainMenu()

    if selection == 1:
        print('Starting NEW GAME')
        RunGame(0)      

    elif selection == 2:
        #RunGame(1)
        print('LOAD GAME not yet implemented.\n')
        MainMenu()

    elif selection == 3:
        util.scroll3(0.005, 60, 'GloryDaze is a text only adventure.  '+
        'That means there are no graphics! Everything about the game '+
        'will be displayed on the screen. Want to do something? Just '+
        'type it in! (a ">" symbol means the game is waiting for your '+
        'input). The game allows for as much natural language as possible '+
        'but if you\'re having trouble getting around, try shorter sentences '+
        'like "open door" or "push button". (NOT IMPLEMENTED) At any '+
        'point during the game, type "savegame" to save your progress '+
        'or "help" for help.  Have fun!\n')
        MainMenu()

    elif selection == 4:
        print('Have a nice day!')
        quit()

    else:
        print('Please input a valid integer 1, 2, 3, or 4')
        MainMenu()



MainMenu()

