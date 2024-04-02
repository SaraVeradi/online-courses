#MY  Program
# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
SHIP_ANGLE_VEL_INC = math.pi / 45.0
SHIP_ANGLE = math.pi / 2.0
SHIP_ACCELERATION = 0.2
FRICTION = 0.02
MAX_ROTATION_VEL = 11
MAX_MOVEMENT_VEL = 180
MISSILE_VEL = 4
score = 0
lives = 3
time = 0
directions = [[1,1], [1,-1], [-1,1], [-1,-1]]

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.5)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrust_sound = ship_thrust_sound
        self.acc = 0
        self.forward_vec = angle_to_vector(self.angle)
        
    def draw(self,canvas):
        ''' draw the ship with thrust or without thrust using a tiled image'''
        if not self.thrust :
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        elif self.thrust :
            canvas.draw_image(self.image, [3 * self.image_center[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)

    def angle_vel_change(self, angular_amount):
    
        ''' change the angular velocity by a fixed amount indicated as a global'''
        self.angle_vel += angular_amount
        
        
    def is_thrust(self, boolean_flag):
    
        ''' determine if the ship is thructing and play or rewind the sound'''
        self.thrust = boolean_flag
        if self.thrust:
            self.thrust_sound.play()
        else :
            self.thrust_sound.rewind()
    
    def update(self):
        
        #set the acceleration
        if self.thrust :
            self.acc = SHIP_ACCELERATION
        else :
            self.acc = 0
            
        #update ship's velocity and position
        self.forward_vec = angle_to_vector(self.angle)
        self.vel[0] = (1- FRICTION) * self.vel[0] + self.acc * self.forward_vec[0]
        self.vel[1] = (1- FRICTION) * self.vel[1] + self.acc * self.forward_vec[1]
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1] ) % HEIGHT
        self.angle += self.angle_vel
        
    def shoot_missile(self):
        global a_missile
        missile_position = [0,0]
        missile_position[0] = self.pos[0] + self.forward_vec[0] * self.image_size[0] / 2
        missile_position[1] = self.pos[1] + self.forward_vec[1] * self.image_size[1] / 2
#        a_vel = [MISSILE_VEL * self.vel[0], MISSILE_VEL * self.vel[1]]
        a_vel = [0,0]
        a_vel[0] = self.vel[0] + MISSILE_VEL * angle_to_vector(self.angle)[0]
        a_vel[1] = self.vel[1] + MISSILE_VEL * angle_to_vector(self.angle)[1]
        a_missile = Sprite(missile_position , a_vel, 0, 0, missile_image, missile_info, missile_sound)
        

    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0] ,pos[1] ]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    #draw scores
    canvas.draw_text('Lives', [60, 70], 30, 'white')
    canvas.draw_text(str(lives), [60, 110], 30, 'white')
    canvas.draw_text('Score', [WIDTH - 100, 70], 30, 'white')
    canvas.draw_text(str(score), [WIDTH - 100, 110], 30, 'white')

    
#key handlers
def keydown(key):

    if simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel_change( SHIP_ANGLE_VEL_INC )
    elif simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel_change( -SHIP_ANGLE_VEL_INC )
    elif simplegui.KEY_MAP["up"] == key :
        my_ship.is_thrust(True)
    elif simplegui.KEY_MAP["space"] == key :
        my_ship.shoot_missile()



        
def keyup(key):
    if simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel_change( -SHIP_ANGLE_VEL_INC )
    elif simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel_change( +SHIP_ANGLE_VEL_INC )
    elif simplegui.KEY_MAP["up"] == key :
        my_ship.is_thrust(False)
      
        
        
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    rock_pos = [random.randrange(WIDTH),random.randrange(HEIGHT)]
    ang_vel_direction = random.choice(directions)
    rock_ang_vel = ang_vel_direction[0] * random.randrange(MAX_ROTATION_VEL) / 60.0 
    rock_vel = [random.randrange(MAX_MOVEMENT_VEL) / 60.0 ,random.randrange(MAX_MOVEMENT_VEL) / 60.0]
    rock_vel_direction = random.choice(directions)
    rock_vel[0] *= rock_vel_direction[0]
    rock_vel[1] *= rock_vel_direction[1]
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], SHIP_ANGLE, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0], 0, 0.09, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [1,1], 0, 0.02, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
