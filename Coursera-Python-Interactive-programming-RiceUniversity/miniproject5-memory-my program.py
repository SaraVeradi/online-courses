# implementation of card game - Memory

import simplegui
import random

FWIDTH = 800  #frame heiht and width
FHEIGHT = 100
CARD_WIDTH = FWIDTH / 16

# helper function to initialize globals
def new_game():
    global cards, exposed, state, fliped, turns
    state = 0
    turns = 0
    fliped = [None, None]      #Index of fliped cards
    cards = range(1,9)         #2 sets of cards
    cards.extend(range(1,9))
    random.shuffle(cards)

    exposed = []
    for idx in range(0,16):
        exposed.append(False)

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, fliped, state, turns
    position = list(pos)
    card_num = position[0] / CARD_WIDTH
    
    if not exposed[card_num] :
        turns += 1
        if state == 0 :
            state = 1
            exposed[card_num] = True
            fliped[0] = card_num
        elif state == 1:
            state = 2
            exposed[card_num] = True
            fliped[1] = card_num
        elif state == 2  :
            if cards[fliped[0]] != cards[fliped[1]]:
                exposed[fliped[0]] = False
                exposed[fliped[1]] = False
            state =1
            exposed[card_num] = True
            fliped[0] = card_num
   
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):

    for idx in range(len(cards)):
        if exposed[idx] :
            num_pos = [idx * CARD_WIDTH + 13, 70]
            canvas.draw_text(str(cards[idx]), num_pos, 30, "white"  )
        else :
            CARD_POINT = idx * CARD_WIDTH
            point1 = [CARD_POINT, 0]       ; point2 = [CARD_POINT + CARD_WIDTH, 0]
            point3 = [CARD_POINT, FHEIGHT] ; point4 = [CARD_POINT + CARD_WIDTH, FHEIGHT]
            canvas.draw_polygon([point1, point2, point4, point3], 1, 'Orange', 'Green')

    label.set_text( "Tunrs = " + str(turns / 2 + turns % 2))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0" )

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric