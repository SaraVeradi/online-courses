# ============================================================================ #
#                                                                              #
# MINI-PROJECT #8                                                              #
# Implementation of the 'game' RiceRocks - complete  version                   #
# v1.0                                                                         #
#                                                                              #
# GPLv3 - http://www.gnu.org/licenses/gpl-3.0.html - except images & audio     #
# See game assets in the code below to read assets license/use rights.         #
#                                                                              #
# By J.F. Candido Filho                                                        #
#                                                                              #
# Date: 2015/08/09                                                          #
#                                                                              #
# ---------------------------------------------------------------------------- #
#                                                                              #
# This follows the grading rubrics proposed. This refers to:                   #
#                                                                              #
#	An Introduction to Interactive Programming in Python (Part 2)              #
#	by Joe Warren, Scott Rixner, John Greiner, Stephen Wong                    #
#	Rice University                                                            #
#                                                                              #
# 	LINK: https://class.coursera.org/interactivepython2-003                    #
#                                                                              #
# ---------------------------------------------------------------------------- #
# THIS CODE WAS TESTED ON GOOGLE CHROME (44.x) ON WINDOWS 8.1                  #
# ============================================================================ #


# LIBRARIES
# #########

import simplegui
import math
import random


# CLASSES
# #######

class ImageInfo:
    """
    Definitions of the class `ImageInfo`.
    """

    def __init__( self, center, size, radius = 0, lifespan = None, animated = False ):
        """
        Initiates the instance of the object `ImageInfo`.
        """
    
        # Image's definitions
        self.center = center
        self.size = size
        
        # Image's interactive caracteristics
        self.radius = radius
        
        # Check if there is lifespan ( duration )
        if lifespan:
        
            # Set lifespan to the desired value
            self.lifespan = lifespan
            
        # If not..    
        else:
        
            # .. set lifespan (duration) to be infinite
            self.lifespan = float( 'inf' )
        
        # Set the image to be animated
        self.animated = animated

    def get_center( self ):
        """
        Gets image's center point.
        """
        
        return self.center

    def get_size( self ):
        """
        Gets image's sizes (width and height).
        """
        
        return self.size

    def get_radius( self ):
        """
        Gets image's radius for interaction with other objects.
        """
        
        return self.radius

    def get_lifespan( self ):
        """
        Gets image's lifespan (duration).
        """
        
        return self.lifespan

    def get_animated( self ):
        """
        Gets image's animated status.
        """
        
        return self.animated

class Ship:
    """
    Definitions of the class `Ship`.
    """

    def __init__(self, pos, vel, angle, image, info):
        """
        Initiates the instance of the object `Sphip`.
        """
    
        # Ship's linear configuration
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        
        # Ship's angular configuration 
        self.angle = angle
        self.angle_vel = 0
        
        # Ship's thrusts state
        self.thrust = False
        
        # Ship's image definitions
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        
        # Ship's interactive caracteristics
        self.radius = info.get_radius()
        
    def SET_angle_vel( self, value ):
        """
        Set the angular velocity of the ship based on `value`.
        """
    
        self.angle_vel = value
    
    def SET_thrust( self, value ):
        """
        Set the ship's thrusts ON or OFF based on `value`.
        """
    
        self.thrust = value
    
    def GET_position( self ):
        """
        Returns the ship's position.
        """

        return self.pos
        
    def GET_radius( self ):
        """
        Return the ship's radius.
        """
        
        return self.radius
        
    def shoot( self ):
        """
        Shots a missile from the ship's cannon.
        """
    
        # Globals
        global missile_group
        
        # Calculates the distance of the cannon to the center of the ship
        distance =  [
                        math.cos( self.angle ) * ( self.image_size[X] / 2 ),
                        math.sin( self.angle ) * ( self.image_size[Y] / 2 )
                    ]
        
        # Set the position of the missile to that of the cannon's tip
        position =  [ self.pos[X] + distance[X], self.pos[Y] + distance[Y] ]
        
        # Calculates the velocity of the missile
        velocity =  [
                        self.vel[X] + angle_to_vector( self.angle )[X] * 2,
                        self.vel[Y] + angle_to_vector( self.angle )[Y] * 2
                    ]
        
        # Sets the missile's angle to be the same of the ship
        angle = self.angle
        
        # There is no angular velocity for the missile (it's a straight line)
        angular_velocity = 0
        
        # Missile creation
        missile = Sprite( 
                            position,
                            velocity,
                            self.angle,
                            angular_velocity,
                            missile_image,
                            missile_info,
                            missile_sound
                        )

        # Storing the missile
        missile_group.add( missile )
                        
    def draw( self, canvas ):
        """
        Draw the ship's image inside the canvas based on its thrust behavior.
        """

        # Check if the thrusts are ON and..
        if self.thrust:
        
            # .. get the image with the thrusts ON
            image_center = [ self.image_center[X] + self.image_size[X], self.image_center[Y] ]
        
            # Draw the ship with the thrusts ON
            canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        # Do nothing besides..
        else:
        
            # .. drawing the ship with thrusts OFF 
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update( self ):
        """
        Update the ship's position and velocity properly.
        Maintains the ship inside the canvas area.
        """
    
        # Update position
        self.pos = [ self.pos[ index ] + self.vel[ index ] for index in range(2) ]
        
        # Update orientation
        self.angle += self.angle_vel
        
        # Update velocity considering friction
        self.vel = [ self.vel[ index ] * FRICTION_CONSTANT for index in range(2) ]
        
        # Update velocity's acceleration if trusting
        if self.thrust:
        
            # Get the proper acceleration ( forward vector ) based on orientation
            acceleration = angle_to_vector( self.angle )
            
            # Update considering acceleration
            self.vel = [ self.vel[ index ] + acceleration[ index ] * 0.1 for index in range(2) ]

        # Screen Wrapper
        screen_wrapper( self, 2 )

class Sprite:
    """
    Definitions of the class `Sprite`.
    """

    def __init__( self, pos, vel, ang, ang_vel, image, info, sound = None ):
        """
        Initiates the instance of the object `Sprite`.
        """
    
        # Sprite's linear configuration
        self.pos            = [ pos[0], pos[1] ]
        self.vel            = [ vel[0], vel[1] ]
        
        # Sprite's angular configuration
        self.angle          = ang
        self.angle_vel      = ang_vel
        
        # Sprite's image definitions
        self.image          = image
        self.image_center   = info.get_center()
        self.image_size     = info.get_size()
        self.animated       = info.get_animated()
        
        # Sprite's interactive caracteristics
        self.radius         = info.get_radius()
        self.lifespan       = info.get_lifespan()
        self.age            = 0
        
        # If the sprite has a sound, play it from the beginning
        if sound:
        
            sound.rewind()
            sound.play()

    def GET_position( self ):
        """
        Returns the sprite's position.
        """
        
        return self.pos
    
    def GET_radius( self ):
        """
        Returns the sprite's radius.
        """
        
        return self.radius
        
    def collide( self, object ):
        """
        Returns true if the `self` object collides with the other `object` .
        Returns false otherwise.
        """
        
        obj_position = object.GET_position()
        obj_radius = object.GET_radius()
        
        distance_two_points = dist( obj_position, self.pos )
        
        if obj_radius + self.radius >= distance_two_points:
        
            return True
            
        else:
        
            return False

    def draw( self, canvas ):
        """
        Draw the sprite's image properly inside the canvas.
        """
    
        canvas.draw_image( self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle )
    
    def update( self ):
        """
        Update the sprite's position and orientation properly.
        Maintains the sprite inside the canvas area.
        """
        
        # Update position
        self.pos = [ self.pos[ index ] + self.vel[ index ] for index in range(2) ]
        
        # Update orientation
        self.angle += self.angle_vel

        # Screen Wrapper
        screen_wrapper( self, 2 )
        
        # Increase sprite's age
        self.age += 1
        
        # Check if the sprite is too old
        if self.age >= self.lifespan:
        
            return True
            
        else:
        
            return False


# GLOBALS
# #######

# User interface
DIMENSION           = [ 800, 600 ]
score               = 0
lives               = 3
time                = 0
BEST_SCORE          = 0

# Ship
ANGLE_VEL           = ( math.pi * 2 ) / 60 # 60fps | 2*pi comes from circ length
FRICTION_CONSTANT   = 1 - 0.01
SHIP_AREA           = None # Ship's spawn region

# Rock
MAXIMUM_ROCK_NUMBER = 12

# Cartesian axis
X                   = 0
Y                   = 1

# Objects
my_ship             = None
rock_group          = None
missile_group       = None

# Game state
IN_PLAY             = False

"""
 Game assets:

    Notes:

        Art assets created by Kim Lathrop.
        May be freely re-used in non-commercial projects if Kim is credited.
        
        Sound assets purchased from sounddogs.com.
        Please, do not redistribute as the license does not permit.

    Debris images list:

        - debris1_brown.png
        - debris2_brown.png
        - debris3_brown.png
        - debris4_brown.png
        - debris1_blue.png
        - debris2_blue.png
        - debris3_blue.png
        - debris4_blue.png
        - debris_blend.png
        
    Nebula images list:

        - nebula_brown.png
        - nebula_blue.png
        
    Missile images list:

        - shot1.png
        - shot2.png
        - shot3.png
        
    Asteroid images list:

        - asteroid_blue.png
        - asteroid_brown.png
        - asteroid_blend.png
        
    Animated explosions list:

        - explosion_orange.png
        - explosion_blue.png
        - explosion_blue2.png
        - explosion_alpha.png
"""

# Debris
debris_info         = ImageInfo( [ 320, 240 ], [ 640, 480 ] )
debris_image        = simplegui.load_image( "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png" )

# Nebula
nebula_info         = ImageInfo( [ 400, 300 ], [ 800, 600 ] )
nebula_image        = simplegui.load_image( "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png" )

# Splash
splash_info         = ImageInfo( [ 200, 150 ], [ 400, 300 ] )
splash_image        = simplegui.load_image( "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png" )

# Ship
ship_info           = ImageInfo( [ 45, 45 ], [ 90, 90 ], 35 )
ship_image          = simplegui.load_image( "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png" )

# Missile
missile_info        = ImageInfo( [ 5, 5 ], [ 10, 10 ], 3, 50 )
missile_image       = simplegui.load_image( "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png" )

# Asteroid
asteroid_info       = ImageInfo( [ 45, 45 ], [ 90, 90 ], 40 )
asteroid_image      = simplegui.load_image( "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png" )

# Explosion
explosion_info      = ImageInfo( [ 64, 64 ], [ 128, 128 ], 17, 24, True )
explosion_image     = simplegui.load_image( "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png" )

# Music - ambient
soundtrack          = simplegui.load_sound( "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3" )

# Sounds
missile_sound       = simplegui.load_sound( "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3" )
ship_thrust_sound   = simplegui.load_sound( "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3" )
explosion_sound     = simplegui.load_sound( "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3" )


# HELPER FUNCTIONS
# ################

# - Note: These helper functions handles transformations

def angle_to_vector( angle ):
    """
    Calculates the foward vector of the ship based on it's orientation.
    This orientation comes from the `angle` the ship's image is rotated.
    """
    
    # Returns the calculated vector
    return [ math.cos( angle ), math.sin( angle ) ]

def dist( p, q ):
    """
    Calculates de distance between two points `p` and `q`.
    """
    
    # Returns the calculated vector of the distance.
    return math.sqrt( (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 )

def screen_wrapper( self, range_value = 2 ):
    """
    Wraps the object to a correct position.
    This supposes that a moving object can't go off the screen and warp to the
    opposite side of that it was going off-screen.
    """

    # Loop through the X and Y axis to wrap the 'object' correctly
    for axis in range( range_value ):

        # Use object's image's center as warp-point (like in instructors' video)
        position_rt = self.pos[axis]
        
        # Use object's extremities as warp-point / UNCOMMENT TO USE
        #position_rt = self.pos[axis] - ( self.image_size[axis] / 2 )
    
    
        # Use object's image's center as warp-point (like in instructors' video)
        position_lb = self.pos[axis]
        
        # Use object's extremities as warp-point / UNCOMMENT TO USE
        #position_lb = self.pos[axis] + ( self.image_size[axis] / 2 )
    
    
        # Check for Right or Top area (same behavior)
        if self.vel[axis] <= 0 and position_rt <= 0:
            
            # Set the proper position to be wrapped on
            self.pos[axis] = DIMENSION[axis] + self.pos[axis]
        
        # Check for Left or Bottom area (same behavior)
        elif self.vel[axis] > 0 and position_lb >= DIMENSION[axis]:
    
            # Set the proper position to be wrapped on
            self.pos[axis] = self.pos[axis] - DIMENSION[axis]

def in_region( region, obj_pos ):
    """
    Verify if an object is inside a given region.
    Splash region: [ x -> [0,1], y -> [0,1] ]
    Object position is a point (x,y)
    """
    
    # Calculates if the object position is inside the region
    in_x_region = region[X][0] <= obj_pos[X] and obj_pos[X] <= region[X][1]
    in_y_region = region[Y][0] <= obj_pos[Y] and obj_pos[Y] <= region[Y][1]
    
    # If it is inside, it returns true
    if in_x_region and in_y_region: return( True );
    
    # Else, it returns false
    else: return( False );

def splash_screen_region():
    """
    Defines the region of the Splash screen.
    """
    
    # Get the splash image definitions
    splash_center = ( DIMENSION[X] / 2, DIMENSION[Y] / 2 )
    splash_size = splash_info.get_size()
    
    print splash_center, splash_size

    # Defines the splash region
    splash_region = (
                        (
                            splash_center[X] - (splash_size[X] / 2),
                            splash_center[X] + (splash_size[X] / 2)
                        ),
                        (
                            splash_center[Y] - (splash_size[Y] / 2),
                            splash_center[Y] + (splash_size[Y] / 2)
                        )
                    )
                    
    # Return the splash region
    return( splash_region )

def process_sprite_group( canvas, sprite_set ):
    """
    Draw and update a set of sprites.
    """
    
    # Create a copy of the sprite set to iterate over
    sprite_set_copy = set( sprite_set )
    
    # Iterate through the sprite set
    for sprite in sprite_set_copy:
    
        # Draw and update the sprite set
        sprite.draw( canvas )
        too_old = sprite.update()
        
        # If the sprite is too old..
        if too_old:
        
            # .. remove it.
            sprite_set.remove( sprite )

def group_collide( set_group, sprite_object ):
    """
    Detects collision between a sprite object and elements in a set.
    """
    
    # Makes a copy of the set group
    set_group_copy = set( set_group )
    
    # Iterate through the set group
    for obj in set_group_copy:
    
        # Check if a collision happened
        if obj.collide( sprite_object ):
        
            # Remove the colliding object
            set_group.remove( obj )
            
            # Indicates a collision occurred 
            return True
    
    # No colision occurred
    return False

def group_group_collide( set_group_one, set_group_two ):
    """
    Check for collision between objects of two groups.
    Removes collided object from group one.
    Returns the total ammount of collisions.
    """
    
    # Counts the quantity of removed objects from group one
    count = 0
    
    # Creates a copy of the first group to avoid errors
    set_group_one_copy = set( set_group_one )
    
    # Iterate through each object of the first group
    for obj in set_group_one_copy:
    
        # Check for collision between the object and the second group
        in_collision = group_collide( set_group_two, obj )
        
        # If a collision happened..
        if in_collision:
        
            # .. increase the count of ocurrences by one
            count += 1
            
            # Romeve the object that collided 
            set_group_one.discard( obj )
    
    # Returns the total ammount of collisions    
    return count

def configure_ship_area():
    """
    Configures a region for the ship to be safe from rock spawns.
    """
    
    # Globals
    global SHIP_AREA
    
    # Get ship's position
    ship_pos = my_ship.GET_position()

    # Set ship's area (region)
    SHIP_AREA = [
                    [ ( ship_pos[X] / 2 ) - 100, ( ship_pos[X] / 2 + 100 ) ],
                    [ ( ship_pos[Y] / 2 ) - 100, ( ship_pos[Y] / 2 + 100 ) ]
                ]

                
# EVENT HANDLERS
# ##############

def HANDLER_draw( canvas ):
    """
    Draws the ship, the rock and the missile inside canvas area.    
    """

    # Globas
    global time, lives, score, BEST_SCORE
    
    # Draw animiated background
    time += 1
    wtime = (time / 4) % DIMENSION[X]
    
    center = debris_info.get_center()
    size = debris_info.get_size()
    
    canvas.draw_image   (
                            nebula_image,
                            nebula_info.get_center(),
                            nebula_info.get_size(),
                            [ DIMENSION[X] / 2, DIMENSION[Y] / 2 ],
                            [ DIMENSION[X], DIMENSION[Y] ]
                        )
    
    canvas.draw_image   (
                            debris_image,
                            center,
                            size,
                            ( wtime - DIMENSION[X] / 2, DIMENSION[Y] / 2 ),
                            ( DIMENSION[X], DIMENSION[Y] )
                        )
    
    canvas.draw_image   (
                            debris_image,
                            center,
                            size,
                            ( wtime + DIMENSION[X] / 2, DIMENSION[Y] / 2 ),
                            ( DIMENSION[X], DIMENSION[Y] )
                        )
    
    
    
    # Check if the game is in play
    if IN_PLAY:
    
        # Draw and update ship
        my_ship.draw(canvas)
        my_ship.update()

        # Draw and update rock group
        process_sprite_group( canvas, rock_group )

        # Detects collision between the ship and the group of rocks
        if group_collide( rock_group, my_ship ):

            lives -= 1
            
            if lives <= 0:
            
                INIT()

        # Draw and update missile
        process_sprite_group( canvas, missile_group )

        # Detects collision between rocks and missiles and increments the score
        score += group_group_collide( rock_group, missile_group )
        
        if BEST_SCORE < score:
        
            BEST_SCORE = score
        
        # Draw lives
        canvas.draw_text    (
                                "Lives: " + str( lives ),
                                [ 5, 20 ],
                                20,
                                "White",
                                "monospace"
                            )

        # Draw score
        canvas.draw_text    (
                                "Score: " + str( score ),
                                [ DIMENSION[X] - 100, 20 ],
                                20,
                                "White",
                                "monospace"
                            )
                        
    # Check if the game is in play mode
    elif not IN_PLAY:
    
        # Draw splash screen
        canvas.draw_image   (
                                splash_image,
                                splash_info.get_center(),
                                splash_info.get_size(),
                                [ DIMENSION[X] / 2, DIMENSION[Y] / 2 ],
                                splash_info.get_size()
                            )
                            
        # Best score
        canvas.draw_text    (
                                "Best Score",
                                [ DIMENSION[X] / 2 - 45, 20 ],
                                20,
                                "White",
                                "monospace"
                            )
                            
        canvas.draw_text    (
                                str( BEST_SCORE ),
                                [ DIMENSION[X] / 2, 50 ],
                                30,
                                "#00ddee",
                                "monospace"
                            )

def HANDLER_rock_spawner():
    """
    Time Handler's.
    Spaws a rock after every tick of one second.
    """
    
    # Globals
    global rock_group
    
    # Check if there is space for more rocks
    if len( rock_group ) < MAXIMUM_ROCK_NUMBER and IN_PLAY:
    
        # Defines the rock's 'position'
        position =  [
                    random.randrange( 0, DIMENSION[X] ),
                    random.randrange( 0, DIMENSION[Y] )
                    ]
        
        # Defines the rock's 'velocity'
        velocity =  [ 
                    random.randrange( 0, 5 ) * ( random.randrange( -1, 2, 2) ),
                    random.randrange( 0, 5 ) * ( random.randrange( -1, 2, 2) )
                    ]
        
        # Increase difficulty based on score
        velocity =  [ 
                    velocity[X] * ( 1 + (( score % 10 ) / 10) + (score / 20) ),
                    velocity[Y] * ( 1 + (( score % 10 ) / 10) + (score / 20) )
                    ]
        
        # Defines the rock's image angle
        angle = 0
        
        # Defines the rock's angular velocity
        angular_velocity = random.randrange(0, 21) / 100.0
        
        # Creates the rock's sprite
        rock = Sprite ( 
                            position,
                            velocity,
                            angle,
                            angular_velocity,
                            asteroid_image,
                            asteroid_info
                        )
        
        # Updates ship's safe region
        configure_ship_area()
        
        # Check for instant collision at spawn time of the rock with the ship.
        # Also check if the rock is not too close to the spawn area of the ship.
        if not rock.collide( my_ship ) and not in_region( SHIP_AREA, position ):
        
            # Add the rock to the rock group
            rock_group.add( rock )

def HANDLER_key_down( key ):
    """
    Keyboard key down event handler.
    Set the proper angular velocity for the ship based on it's orientation.
    Set the ship's thruster ON and turn ON the sound.
    Fires a shoot.
    """

    # Globals
    global my_ship

    # Check if in play mode
    if IN_PLAY:
    
        # Sets the angular velocity of the ship properly
        if key == simplegui.KEY_MAP['left']:
        
            my_ship.SET_angle_vel( -1 * ANGLE_VEL )
        
        elif key == simplegui.KEY_MAP['right']:
        
            my_ship.SET_angle_vel( ANGLE_VEL )
        
        # Sets the thruster ON and play its sound
        if key == simplegui.KEY_MAP['up']:
        
            my_ship.SET_thrust( True )
            ship_thrust_sound.play()
        
        # Fires a shoot.
        if key == simplegui.KEY_MAP['space']:
        
            my_ship.shoot()

def HANDLER_key_up( key ):
    """
    Keyboard key up event handler.
    Unset the angular velocity for the ship.
    Set the ship's thruster OFF and turn OFF the sound, rewinding it.
    """

    # Globals
    global my_ship
    
    # Verify if in play mode
    if IN_PLAY:
    
        # Unset the angular velocity of the ship
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        
            my_ship.SET_angle_vel( 0 )
        
        # Turn OFF the thurster and rewind its sound
        if key == simplegui.KEY_MAP['up']:
        
            my_ship.SET_thrust( False )
            ship_thrust_sound.rewind()
    
def HANDLER_mouse_click( position ):
    """
    Mouse click event handler.
    Verifies if there was a click inside the splash screen.
    """
    
    # Globals
    global IN_PLAY
    
    # Check if not in play mode
    if not IN_PLAY:

        # Gets the splash screen region
        splash_region = splash_screen_region()
        
        print splash_region, position

        # Check if the click was inside the region.
        if in_region( splash_region, position ):

            # Restart the game
            restart_game()
        

# GAME INIT
# #########

def restart_game():
    """
    Restart the game,putting it into play mode.
    """
    
    # Globals
    global IN_PLAY, score, lives, my_ship, rock_group, missile_group
    
    # Set to be in play mode
    IN_PLAY = True

    # Restart the game
    score = 0
    lives = 3
    
    # Rewindthe soundtrack
    soundtrack.rewind()

    # Play soundtrack
    soundtrack.play()
    
    # Ship
    my_ship = Ship  ( 
                        [ DIMENSION[X] / 2, DIMENSION[Y] / 2 ],
                        [0, 0],
                        (-1) * math.pi / 2,
                        ship_image,
                        ship_info
                    )

    # Creates/updates a ship's area
    configure_ship_area()
    
    # Rock
    rock_group = set([])
    HANDLER_rock_spawner()

    # Missile
    missile_group = set([])
    
    # Set missile sound volume to a proper one
    missile_sound.set_volume(.5)
    

def INIT():
    """
    Inits the game, creating/recreating the necessary elements.
    """
    
    # Globals
    global my_ship, rock_group, missile_group, IN_PLAY
    
    # Resetting globals
    IN_PLAY = False
    my_ship = None
    rock_group = set([])
    missile_group = set([])
    ship_thrust_sound.rewind()
    soundtrack.rewind()


# FRAME
# #####

# Initialize the frame
frame = simplegui.create_frame( "Asteroids", DIMENSION[X], DIMENSION[Y] )

# Initialize the game objects
INIT()

# Register handlers
frame.set_draw_handler( HANDLER_draw )

timer = simplegui.create_timer( 1000.0, HANDLER_rock_spawner )

frame.set_keydown_handler( HANDLER_key_down )
frame.set_keyup_handler( HANDLER_key_up )

frame.set_mouseclick_handler( HANDLER_mouse_click )

# Get things rolling!
timer.start()
frame.start()