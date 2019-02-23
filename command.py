

err = "I can't do that"

def verb_go(GS, obj):
	if obj == 'north' or obj == 'up':
		print('Debug: you entered north or up')

	elif obj == 'south' or obj == 'down':
		print('Debug: south or down')

	elif obj == 'east' or obj == 'right':
		print('Debug: east or right')

	elif obj == 'west' or obj == 'left':
		print('Debug: west or left')

	else:
		print('Can\'t go that way')
        




def command(GS, s):
	if s.subject == 'player':

        #go, stop, look, at, take, help, inventory, savegame, loadgame, talk, ask, open, close, sleep, sneak, walk, run, drop, use, push, pull, eat, drink, grab, pick up
		if s.verb == "go":
			verb_go(GS, s.object)
        
            
	else:
		print(err)







