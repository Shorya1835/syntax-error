

import pygame
import numpy
import random


# intialize the game
pygame.init()

# screen resolution values
x_res = 800
y_res = 802

# create the screen
screen = pygame.display.set_mode((x_res, y_res))

# background
background = pygame.image.load('carfinal2.png')


# camera
xc = 0
yc = 0




# x,y,z to x,y function
def coordsChange(x_world, y_world, z_world, fov_angle):
    global xc, yc
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

# enemy
enemy = pygame.image.load('motorbike.png')
resize_factor=10200
x_enemy_world1=-4/3
x_enemy_world2=0
x_enemy_world3=4/3
z_enemy_world=20
enemy_lanes = random.sample(range(1, 4), 2)
enemyX = []
enemyY = []
scaling=0
def enemy_movement():
    global x_enemy_world1,x_enemy_world3,x_enemy_world2,enemy,z_enemy_world,enemy_img,enemy_lanes,enemyX,enemyY,scaling
    scaling=(20/z_enemy_world)

    enemy_scaled=pygame.transform.scale(enemy,(15*scaling,34*scaling))
    enemy_img = [enemy_scaled, enemy_scaled]
    enemy_x1,enemy_y1 = coordsChange(x_enemy_world1,y_world,z_enemy_world,numpy.pi/2)
    enemy_x2,enemy_y2 = coordsChange(x_enemy_world2,y_world,z_enemy_world,numpy.pi/2)
    enemy_x3,enemy_y3 = coordsChange(x_enemy_world3,y_world,z_enemy_world,numpy.pi/2)
    enemy_x1-=15*scaling*0.5
    enemy_x2-=15*scaling*0.5
    enemy_x3-=15*scaling*0.5
    enemy_y1-=34*scaling
    enemy_y2-=34*scaling
    enemy_y3-=34*scaling

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


def enemy_i(x, y, i):
    global enemy_img
    screen.blit(enemy_img[i], (x, y))

#bullet coordinates
z_bullet0,z_bullet1=1.4,1.8
x_width=0.025
y_width=0.025
bullet_state=False


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

    #x_bullet = numpy.array([x_bullet0, x_bullet1])
    #y_bullet = numpy.array([y_bullet0, y_bullet1])
    #pygame.draw.line(screen, (255, 0,0), (x_bullet01, y_bullet01), (x_bullet11, y_bullet11),5)

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
    #pygame.draw.line(screen, (255, 0,0), (x_bullet0, y_bullet0), (x_bullet1, y_bullet1),5)

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

def main_game_execution():
    global scaling,enemy_lanes,z_enemy_world,enemyX,enemyY,bullet_state,z_bullet1,z_bullet0,x1,x2,x3,x4,xs1,xs2,xs3,xs4,xS1,xS2,xS3,xS4,y1,y2,y3,y4,ys1,ys2,ys3,ys4,yS1,yS2,yS3,yS4,z_world_strip_right,z_world_strip_left,z_world,xc,yc,speed,speed_from_angle
    # FOR AAKASH SPEED WITH ANGLE
    '''speed_from_angle = speed_change(global_angle)'''
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
        #drawing bullet



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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speed = -speed_from_angle
                if event.key == pygame.K_RIGHT:
                    speed = speed_from_angle
                if event.key==pygame.K_SPACE:
                    if bullet_state==False:
                        x_bullet_i=xc
                        bullet_fire(x_bullet_i)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    speed = 0



        # camera change
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

        # enemyloop
        if(z_enemy_world>10):
            enemy_movement()
            for i in range(0, 2):
                enemy_i(enemyX[i], enemyY[i], i)
            z_enemy_world-=0.07

        else:
            enemy_movement()
            for i in range(0, 2):
                enemy_i(enemyX[i], enemyY[i], i)
        enemyX=[]
        enemyY=[]

        #bullet movement

        if z_bullet1 >=10 and bullet_state == True:
            bullet_state = False
            z_bullet0 = 1.4
            z_bullet1 = 1.8
        elif bullet_state == True:
            bullet_movement(x_bullet_i)

        pygame.display.flip()
    pygame.quit()

main_game_execution()

