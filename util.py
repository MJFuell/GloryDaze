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
'''

import pickle
import sys
import textwrap
import time

DELAY = 0.01
MAXLEN = 80

''' accepts text especially large text and will textwrap up to max_length. '''
''' wraps scroll2() to eliminate its awkward syntax '''
def scroll3(delay, max_length, printout):
    scroll2(DELAY, MAXLEN, textwrap.wrap(printout, MAXLEN))

''' expects list of pre-wrapped text of max_length or less. '''
''' wraps scroll() to aid textwrap but resulted in awkward syntax. '''
def scroll2(delay, max_length, printout):
    for wrapped_text in printout:
        scroll(DELAY, MAXLEN, wrapped_text)

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

def main():
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

if __name__ == '__main__':
    main()
