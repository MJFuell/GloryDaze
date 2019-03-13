'''
util.py
utility functions generally helpful for GloryDaze Text Adventure.
started during data format development debug and test.
by: Richard Ratliff

CS467
Winter 2019
Team Keld :: Michael Fuelling, Richard Ratliff, Jordan Riojas

main() contains some test code for some of the utility functions.
    when imported into another python module main() will not execute.
    main() illustrates how to use the utility functions.

Credits:
- https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
'''

import pickle
import sys
import textwrap
import time
import glob
import os

DELAY = 0.001    # make this smaller for a faster scroll
MAXLEN = 80      # maximum line length to print

formatters = {
    'RED'    : '\033[91m',
    'GREEN'  : '\033[92m',
    'YELLOW' : '\033[93m',
    'BLUE'   : '\033[94m',
    'VIOLET' : '\033[95m',
    'CYAN'   : '\033[96m',
    'END'    : '\033[0m',
    'BOLD'   : '\033[1m',
    'BLINK'  : '\033[5m',
    'BLINK2' : '\033[6m',
}

''' accepts text especially large text and will textwrap up to max_length. '''
''' wraps scroll2() to eliminate its awkward syntax '''
def scroll3(delay, max_length, printout):
    scroll2(delay, max_length, textwrap.wrap(printout, max_length))

''' expects list of pre-wrapped text of max_length or less. '''
''' wraps scroll() to aid textwrap but resulted in awkward syntax. '''
def scroll2(delay, max_length, printout):
    for wrapped_text in printout:
        scroll(delay, max_length, wrapped_text)

''' accepts text to brute force wrap at max_length on white space. '''
def scroll(delay, max_length, printout):
    count = 0
    for character in printout:
        if count > max_length and character == ' ':
            count = 0
            sys.stdout.write('\n')
        else:
            sys.stdout.write(character)
        count += 1
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()

''' save objects in order to save the game to restart later '''
def save(object):
    filename = "./data/saves/" + object.get_name() + ".pkl"
    #print("object = ", object.get_name())
    #print("filename = ", filename)
    with open(filename, 'wb') as output:
        pickle.dump(object, output, pickle.HIGHEST_PROTOCOL)

''' load objects in order to resume game '''
def load(object):
    filename = "./data/saves/" + object.get_name() + ".pkl"
    #print("object = ", object.get_name())
    #print("filename = ", filename)
    with open(filename, 'rb') as input:
        pickle.load(object, input, pickle.HIGHEST_PROTOCOL)

''' print title '''
def print_title():
    f = open('./data/artwk/title', 'r')
    file_contents = f.read()
    print('{BLINK}'.format(**formatters))
    print('{BLUE}'.format(**formatters))
    print('{BOLD}'.format(**formatters))
    print(file_contents)
    print('{BLINK2}'.format(**formatters))
    print('{END}'.format(**formatters))
    f.close()

''' print title '''
def print_start_menu():
    f = open('./data/artwk/start_menu', 'r')
    file_contents = f.readlines()
    print('{VIOLET}'.format(**formatters))
    print('{BOLD}'.format(**formatters))
    # print(file_contents)
    for line in file_contents:
        #print("file: ", file)
        print(line.strip('|\n').center(60))
    f.close()
    print('{END}'.format(**formatters))

''' print you won '''
def print_you_won():
    f = open('./data/artwk/winner', 'r')
    print('{GREEN}'.format(**formatters))
    print('{BOLD}'.format(**formatters))
    file_contents = f.read()
    print(file_contents)
    f.close()
    print('{END}'.format(**formatters))

''' print sorry you lost '''
def print_sorry_you_lost():
    f = open('./data/artwk/sorry', 'r')
    print('{RED}'.format(**formatters))
    print('{BOLD}'.format(**formatters))
    file_contents = f.read()
    print(file_contents)
    f.close()
    print('{END}'.format(**formatters))

''' print ascii artwork for rooms by passing in their name '''
def print_ascii_art(name):
    f = open(name, 'r')
    print('{BLUE}'.format(**formatters))
    print('{BOLD}'.format(**formatters))
    file_contents = f.read()
    print(file_contents)
    f.close()
    print('{END}'.format(**formatters))

''' true or false - is terminal line size greater than check value '''
def term_lines_gt(check):
    lines = os.popen('tput lines', 'r').readline()
    return(int(lines) > check)

''' true or false - is terminal column size greater than check value '''
def term_cols_gt(check):
    cols  = os.popen('tput cols', 'r').readline()
    return (int(cols) > check)

''' perform terminal size check '''
def term_check():
    if (term_lines_gt(23)) and (term_cols_gt(79)):
        print('')
        scroll3(0.1, MAXLEN, ' :) terminal size ok ...')
        print('')
        print('')
        print('')
    else:
        print('')
        scroll3(0.1, MAXLEN, ' :( terminal too small ...')
        print('')
        print('Please resize your terminal terminal to be')
        print('equal or greater than 24 rows 80 columns')
        print('which is often the default terminal size.')
        print('')
        quit()


def main():
    term_check()
    input("Press any key to continue...")
    dir = "./data/artwk/*"
    files = sorted(glob.glob(dir))
    for file in files:
        #print("file: ", file)
        print_ascii_art(file)

    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    scroll(DELAY, MAXLEN, "-" * MAXLEN)
    print("scroll() 80/80 - incorrect")
    scroll(DELAY, MAXLEN, lorem_ipsum)
    scroll(DELAY, MAXLEN, "-" * MAXLEN)
    print("scroll() 70/80 - ok but could be incorrect")
    scroll(DELAY, 70, lorem_ipsum)
    scroll(DELAY, MAXLEN, "-" * MAXLEN)
    # scroll(DELAY, MAXLEN, textwrap.fill(lorem_ipsum, MAXLEN)) # bad
    print("print() textwrap.fill() 80 - good with print() bad with scroll()")
    print(textwrap.fill(lorem_ipsum, MAXLEN))
    scroll(DELAY, MAXLEN, "-" * MAXLEN)
    print("scroll() textwrap.wrap() 80 - good but loop required for wrapped text")
    for wrapped_text in textwrap.wrap(lorem_ipsum, MAXLEN):
        scroll(DELAY, MAXLEN, wrapped_text)
    scroll(DELAY, MAXLEN, "-" * MAXLEN)
    print("scroll2() textwrap.wrap() 80 - good but awkward syntax")
    scroll2(DELAY, MAXLEN, textwrap.wrap(lorem_ipsum, MAXLEN))  # note this is scroll2()
    scroll(DELAY, MAXLEN, "-" * MAXLEN)
    print("scroll3() 80 - best for long wrapped text")
    scroll3(DELAY, MAXLEN, lorem_ipsum)  # note this is scroll3()
    scroll(DELAY, MAXLEN, "-" * MAXLEN)

    print_title()

if __name__ == '__main__':
    main()
