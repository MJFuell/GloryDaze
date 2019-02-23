

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
        
        
def verb_eat(GS, obj):
	print(err)     
        
def verb_stop(GS, obj):
	print(err)
        
def verb_eat(GS, obj):
	print(err)
        
def verb_look(GS, obj):
	print(err)
        
def verb_at(GS, obj):
	print(err)
        
def verb_take(GS, obj):
	print(err)
        
def verb_help(GS, obj):
	print(err)
        
def verb_inventory(GS, obj):
	print(err)
        
def verb_savegame(GS, obj):
	print(err)
        
def verb_loadgame(GS, obj):
	print(err)
        
def verb_talk(GS, obj):
	print(err)
        
def verb_ask(GS, obj):
	print(err)
        
def verb_open(GS, obj):
	print(err)
        
def verb_close(GS, obj):
	print(err)
        
def verb_sleep(GS, obj):
	print(err)
        
def verb_sneak(GS, obj):
	print(err)
        
def verb_walk(GS, obj):
	print(err)
        
def verb_run(GS, obj):
	print(err)
        
def verb_drop(GS, obj):
	print(err)
        
def verb_use(GS, obj):
	print(err)
        
def verb_push(GS, obj):
	print(err)
        
def verb_pull(GS, obj):
	print(err)
        
def verb_eat(GS, obj):
	print(err)
        
def verb_drink(GS, obj):
	print(err)
        
def verb_grab(GS, obj):
	print(err)
        
def verb_pick_up(GS, obj):
	print(err)




def command(GS, s):
	if s.subject == 'player':

        #go, stop, look, at, take, help, inventory, savegame, loadgame, talk, ask, open, close, sleep, sneak, walk, run, drop, use, push, pull, eat, drink, grab, pick up
		if s.verb == "go":
			verb_go(GS, s.object)
        
            
	else:
		print(err)







