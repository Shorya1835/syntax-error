import threading
import detector
import pygame
import numpy
import random
import time

#print(d.shoot, d.angle)

camera_state = True

#screen resolution values
x_res = 800
y_res = 802

# camera
xc = 0
yc = 0

# x,y,z of real world to x,y of screen function
def coordsChange(x_world, y_world, z_world, fov_angle):
    global xc, yc, x_res, y_res
    z_world = max(1, z_world)
    scaling_x = (x_res / 2) / (numpy.tan(fov_angle / 2))
    scaling_y = (y_res / 2) / (numpy.tan(fov_angle / 2))
    x_screen = x_res * .5 * (1 + ((x_world - xc) / (numpy.tan(fov_angle / 2) * z_world)))
    y_screen = y_res * .5 * (1 - ((y_world - yc) / (numpy.tan(fov_angle / 2) * z_world)))
    return x_screen, y_screen


# road
x_world=numpy.array([-2,2,2,-2])
y_world=-0.5
z_world=numpy.array([20,20,1.4,1.4])


x1, y1 = coordsChange(x_world[0], y_world, z_world[0], numpy.pi / 2)
x2, y2 = coordsChange(x_world[1], y_world, z_world[1], numpy.pi / 2)
x3, y3 = coordsChange(x_world[2], y_world, z_world[2], numpy.pi / 2)
x4, y4 = coordsChange(x_world[3], y_world, z_world[3], numpy.pi / 2)

# stripe left

xS1, xS2, xS3, xS4 = 420, 430, 440, 430
yS1, yS2, yS3, yS4 = 235, 235, 250, 250
x_world_strip_left=numpy.array([-2 / 3 - 0.05,-2 / 3 + 0.05,-2 / 3 + 0.05,-2 / 3 - 0.05])
z_world_strip_left=numpy.array([18,18,20,20])

xs1, ys1 = coordsChange(x_world_strip_left[0], y_world, z_world_strip_left[0], numpy.pi / 2)
xs2, ys2 = coordsChange(x_world_strip_left[1], y_world, z_world_strip_left[1], numpy.pi / 2)
xs3, ys3 = coordsChange(x_world_strip_left[2], y_world, z_world_strip_left[2], numpy.pi / 2)
xs4, ys4 = coordsChange(x_world_strip_left[3], y_world, z_world_strip_left[3], numpy.pi / 2)

# stripe right
x_world_strip_right=numpy.array([+2 / 3 - 0.05,+2 / 3 + 0.05,+2 / 3 + 0.05,+2 / 3 - 0.05])
z_world_strip_right=numpy.array([18,18,20,20])


xS1, yS1 = coordsChange(x_world_strip_right[0], y_world, z_world_strip_right[0], numpy.pi / 2)
xS2, yS2 = coordsChange(x_world_strip_right[1], y_world, z_world_strip_right[1], numpy.pi / 2)
xS3, yS3 = coordsChange(x_world_strip_right[2], y_world, z_world_strip_right[2], numpy.pi / 2)
xS4, yS4 = coordsChange(x_world_strip_right[3], y_world, z_world_strip_right[3], numpy.pi / 2)

# Enemy
enemy = pygame.image.load('motorbike.png')
resize_factor=10200
x_enemy_world1=-4/3
x_enemy_world2=0
x_enemy_world3=4/3
x_enemy_world_list=[-4/3,0,4/3]
z_enemy_world=[20,20]
enemy_lanes = random.sample(range(1, 4), 2)
enemyX = []
enemyY = []
scaling=[]

#enemy movement function
def enemy_movement(z_enemy_w):
    global x_enemy_world1,x_enemy_world3,x_enemy_world2,enemy,enemy_img,enemy_lanes,enemyX,enemyY,scaling
    scaling.append(20/z_enemy_w)
    a=(20/z_enemy_w)
    enemy_scaled=pygame.transform.scale(enemy,(15*a,34*a))
    enemy_img = [enemy_scaled, enemy_scaled]
    enemy_x1,enemy_y1 = coordsChange(x_enemy_world1,y_world,z_enemy_w,numpy.pi/2)
    enemy_x2,enemy_y2 = coordsChange(x_enemy_world2,y_world,z_enemy_w,numpy.pi/2)
    enemy_x3,enemy_y3 = coordsChange(x_enemy_world3,y_world,z_enemy_w,numpy.pi/2)
    enemy_x1-=15*a*0.5
    enemy_x2-=15*a*0.5
    enemy_x3-=15*a*0.5
    enemy_y1-=34*a
    enemy_y2-=34*a
    enemy_y3-=34*a

    for i in enemy_lanes:
        if i == 1:
            enemyX.append(enemy_x1)
            enemyY.append(enemy_y1)
        elif i == 2:
            enemyX.append(enemy_x2)
            enemyY.append(enemy_y2)
        elif i == 3:
            enemyX.append(enemy_x3)
            enemyY.append(enemy_y3)

#putting enemy on screen
def enemy_i(x, y, i):
    global enemy_img
    screen.blit(enemy_img[i], (x, y))

#bullet coordinates
z_bullet0,z_bullet1=1.4,1.8
x_width=0.025
y_width=0.050
bullet_state=False
bullet_count=10
count=0

#bullet firing function
def bullet_fire(x_bullet_i):
    global bullet_state,x_width,y_width
    bullet_state = True
    x_bullet01, y_bullet01 = coordsChange(x_bullet_i-x_width, y_world+y_width, z_bullet0, numpy.pi / 2)
    x_bullet02, y_bullet02 = coordsChange(x_bullet_i+x_width, y_world+y_width, z_bullet0, numpy.pi / 2)
    x_bullet03, y_bullet03 = coordsChange(x_bullet_i + x_width, y_world - y_width, z_bullet0, numpy.pi / 2)
    x_bullet04, y_bullet04 = coordsChange(x_bullet_i - x_width, y_world - y_width, z_bullet0, numpy.pi / 2)
    x_bullet11, y_bullet11 = coordsChange(x_bullet_i - x_width, y_world + y_width, z_bullet1, numpy.pi / 2)
    x_bullet12, y_bullet12 = coordsChange(x_bullet_i + x_width, y_world + y_width, z_bullet1, numpy.pi / 2)
    x_bullet13, y_bullet13 = coordsChange(x_bullet_i + x_width, y_world - y_width, z_bullet1, numpy.pi / 2)
    x_bullet14, y_bullet14 = coordsChange(x_bullet_i - x_width, y_world - y_width, z_bullet1, numpy.pi / 2)
    pygame.draw.polygon(screen,(255,0,0),[(x_bullet01,y_bullet01),(x_bullet02,y_bullet02),(x_bullet03,y_bullet03),(x_bullet04,y_bullet04)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet01, y_bullet01), (x_bullet11, y_bullet11), (x_bullet12, y_bullet12),
                         (x_bullet02, y_bullet02)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet02, y_bullet02), (x_bullet03, y_bullet03), (x_bullet13, y_bullet13),
                         (x_bullet12, y_bullet12)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet14, y_bullet14), (x_bullet13, y_bullet13), (x_bullet03, y_bullet03),
                         (x_bullet04, y_bullet04)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet01, y_bullet01), (x_bullet11, y_bullet11), (x_bullet14, y_bullet14),
                         (x_bullet04, y_bullet04)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet11, y_bullet11), (x_bullet12, y_bullet12), (x_bullet13, y_bullet13),
                         (x_bullet14, y_bullet14)])


#updating location of bullet
def bullet_update(x_bullet01,y_bullet01,x_bullet02,y_bullet02,x_bullet03,y_bullet03,x_bullet04,y_bullet04,x_bullet11,y_bullet11,x_bullet12,y_bullet12,x_bullet13,y_bullet13,x_bullet14,y_bullet14):
    global bullet_state
    bullet_state = True
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet01, y_bullet01), (x_bullet02, y_bullet02), (x_bullet03, y_bullet03),
                         (x_bullet04, y_bullet04)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet01, y_bullet01), (x_bullet11, y_bullet11), (x_bullet12, y_bullet12),
                         (x_bullet02, y_bullet02)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet02, y_bullet02), (x_bullet03, y_bullet03), (x_bullet13, y_bullet13),
                         (x_bullet12, y_bullet12)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet14, y_bullet14), (x_bullet13, y_bullet13), (x_bullet03, y_bullet03),
                         (x_bullet04, y_bullet04)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet01, y_bullet01), (x_bullet11, y_bullet11), (x_bullet14, y_bullet14),
                         (x_bullet04, y_bullet04)])
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x_bullet11, y_bullet11), (x_bullet12, y_bullet12), (x_bullet13, y_bullet13),
                         (x_bullet14, y_bullet14)])


#changing location of bullet
def bullet_movement(x_bullet_i):
    global z_bullet1, z_bullet0,x_width,y_width
    z_bullet0 += 0.3
    z_bullet1 += 0.3
    x_bullet01, y_bullet01 = coordsChange(x_bullet_i - x_width, y_world + y_width, z_bullet0, numpy.pi / 2)
    x_bullet02, y_bullet02 = coordsChange(x_bullet_i + x_width, y_world + y_width, z_bullet0, numpy.pi / 2)
    x_bullet03, y_bullet03 = coordsChange(x_bullet_i + x_width, y_world - y_width, z_bullet0, numpy.pi / 2)
    x_bullet04, y_bullet04 = coordsChange(x_bullet_i - x_width, y_world - y_width, z_bullet0, numpy.pi / 2)
    x_bullet11, y_bullet11 = coordsChange(x_bullet_i - x_width, y_world + y_width, z_bullet1, numpy.pi / 2)
    x_bullet12, y_bullet12 = coordsChange(x_bullet_i + x_width, y_world + y_width, z_bullet1, numpy.pi / 2)
    x_bullet13, y_bullet13 = coordsChange(x_bullet_i + x_width, y_world - y_width, z_bullet1, numpy.pi / 2)
    x_bullet14, y_bullet14 = coordsChange(x_bullet_i - x_width, y_world - y_width, z_bullet1, numpy.pi / 2)
    bullet_update(x_bullet01,y_bullet01,x_bullet02,y_bullet02,x_bullet03,y_bullet03,x_bullet04,y_bullet04,x_bullet11,y_bullet11,x_bullet12,y_bullet12,x_bullet13,y_bullet13,x_bullet14,y_bullet14)

#speed
speed=0
speed_from_angle=0.05
angle_to_accn_factor=0
def speed_change(angle):
    """
    to convert the input angle into final speed
    """
    final_speed = angle_to_accn_factor*angle
    return final_speed

#collison function
def isCollision(bullet_x_i,z_bullet1,z_enemy_world,enemyx):
    distance = numpy.sqrt((enemyx-bullet_x_i)**2+(z_bullet1-z_enemy_world)**2)

    if distance < 3/8:
        return True
    else:
        return False

#obstacle
obstacle=pygame.image.load('barrier.png')
x_obstacle_world1=-4/3
x_obstacle_world2=0
x_obstacle_world3=4/3
z_obstacle=20
list=[1,2,3]
obstacleX=0
obstacleY=0
x_lane=0
x_obs_lane=[-4/3,0,4/3]

#obstacle movement
def obstacle_movement(z_obstacle_r):
    global x_lane,x_obstacle_world1,x_obstacle_world3,x_obstacle_world2,obstacle_lanes,obstacle,obstacleX,obstacleY,obstacle_scaled,list,enemy_lanes, obstacle_choice
    for obstacle_choice_it in list:
        if obstacle_choice_it not in enemy_lanes:
            obstacle_choice=obstacle_choice_it
    a=(20/z_obstacle_r)
    random_scale=5
    obstacle_scaled=pygame.transform.scale(obstacle,(random_scale*a,random_scale*a))

    obstacle_x1,obstacle_y1 = coordsChange(x_obstacle_world1,y_world,z_obstacle,numpy.pi/2)
    obstacle_x2,obstacle_y2 = coordsChange(x_obstacle_world2,y_world,z_obstacle,numpy.pi/2)
    obstacle_x3,obstacle_y3 = coordsChange(x_obstacle_world3,y_world,z_obstacle,numpy.pi/2)
    obstacle_x1-=random_scale*a*0.5
    obstacle_x2-=random_scale*a*0.5
    obstacle_x3-=random_scale*a*0.5
    obstacle_y1-=random_scale*a
    obstacle_y2-=random_scale*a
    obstacle_y3-=random_scale*a


    if obstacle_choice == 1:
        obstacleX=obstacle_x1
        obstacleY=obstacle_y1
        x_lane=1
    elif obstacle_choice == 2:
        obstacleX=obstacle_x2
        obstacleY=obstacle_y2
        x_lane=2
    elif obstacle_choice == 3:
        obstacleX=obstacle_x3
        obstacleY=obstacle_y3
        x_lane=3


def obstacle_i(x, y):
    global obstacle_scaled
    screen.blit(obstacle_scaled, (x, y))

#variablle to check spawning of obstacles
bool=True
r=0
def obs():
    global z_obstacle, r, bool
    z_obstacle -= 0.08
    obstacle_movement(z_obstacle)

    obstacle_i(obstacleX, obstacleY)
    if z_obstacle < 1.4:
        bool = True
        r = 0
        z_obstacle = 20

#collision with obstacle
def collsion_obstacle(x_c,x_obs,z_obs):

    if z_obs<=1.45 and (x_obs<x_c+3/4 and x_obs>x_c-3/4):

        return True
    else:
        return False
x_bullet_i=0

np_arr=numpy.zeros(150)
np_arr[0]=1

#banana obstacle
banana=pygame.image.load('banana.png')
z_banana_world=0
x_world_banana_possible=[-5/3,-1,-1/3,1/3,1,5/3]
banana_lane_possible=[[0,1],[2,3],[4,5]]
banana_lane=0
banana_x=0
banana_y=0
banana_scaled=0
banana_timer=0

#intialize z according to bike
def obs_banana_z():
    global z_banana_world,enemy_lanes,z_enemy_world,banana_lane
    banana_lane1=random.choice(banana_lane_possible[enemy_lanes[0]-1])
    banana_lane2=random.choice(banana_lane_possible[enemy_lanes[1]-1])
    banana_lane=random.choice([banana_lane1,banana_lane2])

    if banana_lane==0:
        z_banana_world=z_enemy_world[enemy_lanes.index(1)]
    elif banana_lane==1:
        z_banana_world=z_enemy_world[enemy_lanes.index(1)]
    elif banana_lane==2:
        z_banana_world=z_enemy_world[enemy_lanes.index(2)]
    elif banana_lane==3:
        z_banana_world=z_enemy_world[enemy_lanes.index(2)]
    elif banana_lane==4:
        z_banana_world=z_enemy_world[enemy_lanes.index(3)]
    elif banana_lane==5:
        z_banana_world=z_enemy_world[enemy_lanes.index(3)]

#change in x and y of real world according to decrease in z of banana
def banana_movement(z_banana_w):
    global list,enemy_lanes,x_world_banana_possible,z_banana_world,banana_scaled,banana_x,banana_y,banana_lane

    a=(20/z_banana_w)
    random_scale=5
    banana_scaled=pygame.transform.scale(banana,(random_scale*a,random_scale*a))

    banana_x1,banana_y1 = coordsChange(x_world_banana_possible[0],y_world,z_banana_w,numpy.pi/2)
    banana_x2,banana_y2 = coordsChange(x_world_banana_possible[1],y_world,z_banana_w,numpy.pi/2)
    banana_x3,banana_y3 = coordsChange(x_world_banana_possible[2],y_world,z_banana_w,numpy.pi/2)
    banana_x4,banana_y4 = coordsChange(x_world_banana_possible[3],y_world,z_banana_w,numpy.pi/2)
    banana_x5,banana_y5 = coordsChange(x_world_banana_possible[4],y_world,z_banana_w,numpy.pi/2)
    banana_x6,banana_y6 = coordsChange(x_world_banana_possible[5],y_world,z_banana_w,numpy.pi/2)
    banana_x1-=random_scale*a*0.5
    banana_x2-=random_scale*a*0.5
    banana_x3-=random_scale*a*0.5
    banana_y1-=random_scale*a
    banana_y2-=random_scale*a
    banana_y3-=random_scale*a
    banana_x4-=random_scale*a*0.5
    banana_x5-=random_scale*a*0.5
    banana_x6-=random_scale*a*0.5
    banana_y4-=random_scale*a
    banana_y5-=random_scale*a
    banana_y6-=random_scale*a
    
    
    if banana_lane==0:
        banana_x=banana_x1
        banana_y=banana_y1
    elif banana_lane==1:
        banana_x=banana_x2
        banana_y=banana_y2
    elif banana_lane==2:
        banana_x=banana_x3
        banana_y=banana_y3
    elif banana_lane==3:
        banana_x=banana_x4
        banana_y=banana_y4
    elif banana_lane==4:
        banana_x=banana_x5
        banana_y=banana_y5
    elif banana_lane==5:
        banana_x=banana_x6
        banana_y=banana_y6

#loading the banana
def banana_i(x, y):
    global banana_scaled
    screen.blit(banana_scaled, (x, y))

bool1=1
r1=0

#decreasing z of banana
def obs_banana():
    global z_banana_world, r1, bool1
    z_banana_world -= 0.08
    banana_movement(z_banana_world)

    banana_i(banana_x, banana_y)
    if z_banana_world < 1.4:
        bool1 = True
        r1 = 0
        z_banana_world = 20
        
#collision check of banana
def collsion_obstacle_banana(x_c,x_obs,z_obs):

    if z_obs<=1.45 and (x_obs<x_c+3/4 and x_obs>x_c-3/4):

        return True
    else:
        return False

np_arr1=numpy.zeros(250)
np_arr1[0]=1

#game over and health
health=100

def game_over_text():
    over_font=pygame.font.Font('freesansbold.ttf',64)
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,300))

#random variable which comes to use afterwards
x_bullet_i=0

def main_game_execution():
    global count,bullet_count,banana_timer,z_banana_world,banana_lane,x_world_banana_possible,nparr1,bool1,r1,health,x_obs_lane,x_lane,np_arr,bool,r, z_obstacle,testX,testY,x_enemy_world_list,x_bullet_i,score_value,scaling,enemy_lanes,z_enemy_world,enemyX,enemyY,bullet_state,z_bullet1,z_bullet0,x1,x2,x3,x4,xs1,xs2,xs3,xs4,xS1,xS2,xS3,xS4,y1,y2,y3,y4,ys1,ys2,ys3,ys4,yS1,yS2,yS3,yS4,z_world_strip_right,z_world_strip_left,z_world,xc,yc,speed,speed_from_angle
    global x_res, y_res
    global screen


    # intialize the game
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((x_res, y_res))

    # background
    background = pygame.image.load('carfinal2.png')
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1)

    #score
    score_value=0
    font = pygame.font.Font('freesansbold.ttf',32)
    textX=10
    textY=10

    #random variable which comes to use afterwards
    x_bullet_i=0

    # game loop
    running = True
    while running:

        # RGB
        screen.fill((0, 0, 0))
        # drawing road
        pygame.draw.polygon(screen, (92, 95, 102), ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))
        # drawing sky
        pygame.draw.rect(screen, (135, 206, 235), (0, 0, x_res, y1))
        # drawing grass
        pygame.draw.polygon(screen, (89, 166, 8), ((0, y1), (x1, y2), (x4, y3), (0, y4)))
        pygame.draw.polygon(screen, (89, 166, 8), ((x2, y1), (x_res, y2), (x_res, y3), (x3, y4)))

        # drawing stripes
        pygame.draw.polygon(screen, (255, 255, 255), ((xs1, ys1), (xs2, ys2), (xs3, ys3), (xs4, ys4)))
        pygame.draw.polygon(screen, (255, 255, 255), ((xS1, yS1), (xS2, yS2), (xS3, yS3), (xS4, yS4)))
        # moving stripes
        pygame.time.wait(9)
        if (z_world_strip_right[2] >= 1):
            z_change=0.1
            z_world_strip_left[0] -= z_change
            z_world_strip_left[1] -= z_change
            z_world_strip_left[2] -= z_change
            z_world_strip_left[3] -= z_change

            xs1, ys1 = coordsChange(x_world_strip_left[0],y_world, z_world_strip_left[0], numpy.pi / 2)
            xs2, ys2 = coordsChange(x_world_strip_left[1], y_world, z_world_strip_left[1], numpy.pi / 2)
            xs3, ys3 = coordsChange(x_world_strip_left[2], y_world, z_world_strip_left[2], numpy.pi / 2)
            xs4, ys4 = coordsChange(x_world_strip_left[3], y_world, z_world_strip_left[3], numpy.pi / 2)

            z_world_strip_right[0] -= z_change
            z_world_strip_right[1] -= z_change
            z_world_strip_right[2] -= z_change
            z_world_strip_right[3] -= z_change

            xS1, yS1 = coordsChange(x_world_strip_right[0], y_world, z_world_strip_right[0], numpy.pi / 2)
            xS2, yS2 = coordsChange(x_world_strip_right[1], y_world, z_world_strip_right[1], numpy.pi / 2)
            xS3, yS3 = coordsChange(x_world_strip_right[2], y_world, z_world_strip_right[2], numpy.pi / 2)
            xS4, yS4 = coordsChange(x_world_strip_right[3], y_world, z_world_strip_right[3], numpy.pi / 2)

        else:
            z_world_strip_left=numpy.array([18,18,20,20])
            z_world_strip_right = numpy.array([18, 18, 20, 20])

            xs1, ys1 = coordsChange(x_world_strip_left[0], y_world, z_world_strip_left[0], numpy.pi / 2)
            xs2, ys2 = coordsChange(x_world_strip_left[1], y_world, z_world_strip_left[1], numpy.pi / 2)
            xs3, ys3 = coordsChange(x_world_strip_left[2], y_world, z_world_strip_left[2], numpy.pi / 2)
            xs4, ys4 = coordsChange(x_world_strip_left[3], y_world, z_world_strip_left[3], numpy.pi / 2)

            xS1, yS1 = coordsChange(x_world_strip_right[0], y_world, z_world_strip_right[0], numpy.pi / 2)
            xS2, yS2 = coordsChange(x_world_strip_right[1], y_world, z_world_strip_right[1], numpy.pi / 2)
            xS3, yS3 = coordsChange(x_world_strip_right[2], y_world, z_world_strip_right[2], numpy.pi / 2)
            xS4, yS4 = coordsChange(x_world_strip_right[3], y_world, z_world_strip_right[3], numpy.pi / 2)

        # background image
        screen.blit(background,(0,540))

        #regarding hand gestures and controls of game
        if camera_state:
            speed = detector.angle * speed_from_angle

        else:
            detector.shoot = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speed = -speed_from_angle
                if event.key == pygame.K_RIGHT:
                    speed = speed_from_angle
                if event.key==pygame.K_SPACE:
                    bullet_sound = pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    detector.shoot = True


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    speed = 0

        #print(detector.shoot, detector.angle)

        if bullet_state==False and detector.shoot and bullet_count>0:
            x_bullet_i=xc
            bullet_fire(x_bullet_i)
            bullet_count-=1


        # camera change
        if(banana_timer>0):
            speed+=random.uniform(-0.05,0.05)
        xc += speed

        # road change
        if (speed != 0):
            x1, y1 = coordsChange(x_world[0], y_world, z_world[0], numpy.pi / 2)
            x2, y2 = coordsChange(x_world[1], y_world, z_world[1], numpy.pi / 2)
            x3, y3 = coordsChange(x_world[2], y_world, z_world[2], numpy.pi / 2)
            x4, y4 = coordsChange(x_world[3], y_world, z_world[3], numpy.pi / 2)

        # boundary
        if xc >= 1.5:
            xc = 1.5
        if xc <= -1.5:
            xc = -1.5

        # enemy and hitting with bullet
        for i in range(0,2):
            collision = isCollision(x_bullet_i, z_bullet1, z_enemy_world[i], x_enemy_world_list[enemy_lanes[i] - 1])

            if collision:

                collision_sound = pygame.mixer.Sound('explosion.wav')
                collision_sound.play()
                bullet_state = False
                z_bullet0 = 1.4
                z_bullet1 = 1.8
                score_value += 1
                z_enemy_world[i] = 20
                empty_lane = 0
                for x in [1, 2, 3]:
                    if x not in enemy_lanes:
                        empty_lane = x
                enemy_lanes[i] = random.choice([enemy_lanes[i], empty_lane])

            if(z_enemy_world[i]>10):
                enemy_movement(z_enemy_world[i])
                enemy_i(enemyX[i], enemyY[i], i)

                z_enemy_world[i]-=0.07
            else:
                enemy_movement(z_enemy_world[i])
                enemy_i(enemyX[i], enemyY[i], i)
            enemyX=[]
            enemyY=[]
            scaling=[]


        #bullet movement

        if z_bullet1 >=20 and bullet_state == True:
            bullet_state = False
            z_bullet0 = 1.4
            z_bullet1 = 1.8
        elif bullet_state == True:
            bullet_movement(x_bullet_i)
        
        #obstacle loop
        if bool:
            r=random.choice(np_arr1)
            if r==1:
                 bool=False
        if r:
            obs()

        collison_obs=collsion_obstacle(xc,x_obs_lane[x_lane-1],z_obstacle)
        if collison_obs:
            health-=10
            
        #banana loop
        k=0
        if bool1:
            r1=random.choice(np_arr1)
            if r1==1:
                bool1=False
                obs_banana_z()
        if r1:
            obs_banana()

        collison_obs=collsion_obstacle(xc,x_world_banana_possible[banana_lane-1],z_banana_world)
        if collison_obs:
            banana_timer=20

        #banana timer
        if banana_timer>0:
            banana_timer-=1
            
        #increasing bullet_count slowly to guard against spam of bullets
        count+=1
        if(count%200==0) and bullet_count<=10:
            bullet_count+=1
            count=0

        #displaying score
        score = font.render("SCORE: " + str(score_value), True, (0, 125, 0))
        screen.blit(score, (textX, textY))
        #displaying bullet_count
        s = font.render("BULLETS: " + str(bullet_count), True, (0, 125, 0))
        screen.blit(s, (textX, textY+70))
        #displaying health adn ending game if health is 0
        health1 = font.render("HEALTH: " + str(health), True, (250, 0, 0))
        screen.blit(health1, (textX, textY + 35))
        if health <= 0:
            screen.fill((0, 0, 0))
            # game over
            over_font = pygame.font.Font('freesansbold.ttf', 64)
            over_text = over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(over_text, (200, 250))
            pygame.time.wait(5000)
            done = False

        #fliiping screen
        pygame.display.flip()
    pygame.quit()
    detector_thread.join()

if __name__ == '__main__':
    
    #creating thread for detector file (init function)
    
    if camera_state:
        detector_thread = threading.Thread(target= detector.detector_init)
        detector_thread.start()

        #wait till game starts and callibration
        while not detector.started:
            time.sleep(0.5)

    main_game_execution()
