# Rock-paper-scissors-lizard-Spock 


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random


# helper functions

def name_to_number(name):
    """
    this is a helper function that converts
    the string 'name' into a number between 0 and 4
    as described above
    """
    
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "name saw invalid strategy", name
    

def number_to_name(number):
    """
    This id a helper function that converts a number
    in the range 0 to 4 into its corresponding name as a string
    as describes at the begining of this code
    """
    
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "number saw invalid  value:",number
        
        
def rpsls(player_choice): 
    """
    determines and prints out the winner given the player's strategy
    and computer's random choice(which will be determined in this function
    """
    
    # printing a blank line to separate consecutive games
    print ""
    
    # printing the player's choice
    print "Player chooses" , player_choice
    
    # converting the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # computing random guess for comp_number using random.randrange()
    comp_number = random.randrange(0 , 5)
    
    # converting comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # printing computer's choice
    print "Computer chooses" , comp_choice
    
    # computing difference of comp_number and player_number modulo five
    result_number = (comp_number - player_number) % 5

    # using if/elif/else to determine winner, printing winner message
    if result_number == 1 or result_number == 2:
        print "Computer wins!"
    elif result_number ==3 or result_number == 4:
        print "Player wins!"
    elif result_number == 0:
        print "Player and computer tie!"
    else:
        print "result_number saw invalid value:", result_number
    
# testing the code 
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")