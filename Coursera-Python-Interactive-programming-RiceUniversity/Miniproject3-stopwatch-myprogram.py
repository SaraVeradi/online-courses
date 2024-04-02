# template for "Stopwatch: The Game"
import simplegui

# define global variables
WIDTH = 300           #width of the frame
HEIGHT = 200          #heigth of the frame
FONT_SIZE = 40        
isrunning = False     #This will be True if the clock is running
tracker = 0           #Time in miliseconds
totalstop = 0         #number of your effort in stopwatch game
successtop = 0        #number of your successful efforts in stopwatch game

#helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

def format(t):
    '''Determines the time in minute:seconds.miliseconds 
    given the time in miliseconds'''
    
    minute = t / (60*10) 
    second = ( t - (minute*600)) // 10
    milisec = t % 10
    
    #Justify the format at witch the time will dispalyed
    if second < 10:
        return str(minute) + ':0' + str(second) + '.' + str(milisec)
    else :
        return str(minute) + ':' + str(second) + '.' + str(milisec)

    
    
# event handlers for buttons; "Start", "Stop", "Reset"

def stop():
    '''stops the timer and determine if you have a successful effort in stopwatch game'''
    
    global totalstop, successtop, isrunning
    timer.stop()
    if isrunning :
        isrunning = False
        totalstop += 1
        if tracker % 10 == 0:
            successtop += 1
    
def start():
    '''starts the timer'''
    
    global isrunning
    isrunning = True
    timer.start()
    
def reset():
    '''resets everything: timer, numbers related to the stopwatch game'''
    
    global tracker, totalstop, successtop, isrunning
    timer.stop()
    isrunning = False
    tracker = 0
    totalstop = 0
    successtop = 0


# define event handler for timer with 0.1 sec interval
def tick():
    ''' keep track of tenthes of a second'''
    
    global tracker
    tracker += 1
    #print tracker #/ 10.0

# define draw handler
def draw(canvas):
    '''Draws the time and numbers of the game.Determine the best position
    for the text so that it will always locate in the middle of the frame'''
    
    x = str(successtop) + '/' + str(totalstop)
    position = WIDTH/2 - frame.get_canvas_textwidth(str(format(tracker)),FONT_SIZE)/2
    canvas.draw_text(format(tracker),[position  , HEIGHT / 2], FONT_SIZE, 'White')
    canvas.draw_text( x, [WIDTH - 70,  30], FONT_SIZE, 'Aqua')
    
# create frame
frame = simplegui.create_frame('Stopwatch', WIDTH , HEIGHT , 100)
timer = simplegui.create_timer(100,tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button('Start', start, 90)
frame.add_button('Stop', stop, 90)
frame.add_button('Reset', reset, 90)

# start frame
frame.start()


# Please remember to review the grading rubric
