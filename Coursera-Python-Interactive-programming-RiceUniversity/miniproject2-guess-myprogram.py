#"Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

#global variable
num_range = 100


# helper function to start and restart the game
def new_game():
    """Starts a new game by Reseting the remaining rounds and secret_number """

    global secret_number
    global remained_guess
    secret_number = random.randrange(0, num_range)
    remained_guess = int(math.ceil(math.log(num_range + 1) / math.log(2)))
    print "New Game!, Range is from 0 to ", num_range
    print "Number of remaining guesses is", remained_guess ; print ""
    

# define event handlers for control panel

def range100():
    """ Changes the range to [0,100) and starts a new game """
    
    global num_range
    num_range = 100
    new_game()
    
    
def range1000():
    """Changes the range to [0,1000) and starts a new game"""
    
    global num_range
    num_range = 1000
    new_game()
    

def input_guess(guess):
    """Gives a proper answer given your input"""
    
    global remained_guess
    global num_range
    guess = int(guess)
    if remained_guess != 0:
        
        remained_guess -= 1
        print "Number of remaining guesses is", remained_guess        
        print "Guess was", guess
        if guess > secret_number:
                print "Lower!\n"
        elif guess < secret_number:
                print "Higher!\n"
        elif guess == secret_number:
                print "Correct!\n"
                num_range = 100
                new_game()
        else:
                print "Error in comapring guess and secret_number", guess, secret_number
    
    if remained_guess == 0:
        print "Game Over!\n"
        new_game()    

                
# create frame
frame = simplegui.create_frame("Guess the number",200,200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess",input_guess,200)

#start frame
frame.start()


# call new_game 
new_game()