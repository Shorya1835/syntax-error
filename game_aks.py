import pygame
import numpy
import random

def coordsChange(x_world,y_world,z_world,fov_angle) -> tuple : ...
def enemy(x,y,i) -> None : ...
def speed_change(angle, initial_speed) -> float : ...


#screen resolution values
x_res=800
y_res=802


angle_to_accn_factor = 10


#create the screen
screen=pygame.display.set_mode((x_res,y_res))

#background
background = pygame.image.load('car.png')


#camera
xc=0
yc=0

#road
x_world1=-2
x_world2=+2
x_world3=+2
x_world4=-2
y_world=-0.5
z_world1=20
z_world2=20
z_world3=1
z_world4=1

x1,y1=coordsChange(x_world1,y_world,z_world1,numpy.pi/2)
x2,y2=coordsChange(x_world2,y_world,z_world2,numpy.pi/2)
x3,y3=coordsChange(x_world3,y_world,z_world3,numpy.pi/2)
x4,y4=coordsChange(x_world4,y_world,z_world4,numpy.pi/2)

#stripe left

xS1,xS2,xS3,xS4=420,430,440,430
yS1,yS2,yS3,yS4=235,235,250,250

x_world_s1=-2/3 - 0.05
x_world_s2=-2/3 + 0.05
x_world_s3=-2/3 + 0.05
x_world_s4=-2/3 - 0.05
z_world_s1=18
z_world_s2=18
z_world_s3=20
z_world_s4=20

xs1,ys1=coordsChange(x_world_s1,y_world,z_world_s1,numpy.pi/2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
xs2,ys2=coordsChange(x_world_s2,y_world,z_world_s2,numpy.pi/2)
xs3,ys3=coordsChange(x_world_s3,y_world,z_world_s3,numpy.pi/2)
xs4,ys4=coordsChange(x_world_s4,y_world,z_world_s4,numpy.pi/2)

#stripe right

x_world_S1=+2/3 - 0.05
x_world_S2=+2/3 + 0.05
x_world_S3=+2/3 + 0.05
x_world_S4=+2/3 - 0.05
z_world_S1=18
z_world_S2=18
z_world_S3=20
z_world_S4=20

xS1,yS1=coordsChange(x_world_S1,y_world,z_world_S1,numpy.pi/2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
xS2,yS2=coordsChange(x_world_S2,y_world,z_world_S2,numpy.pi/2)
xS3,yS3=coordsChange(x_world_S3,y_world,z_world_S3,numpy.pi/2)
xS4,yS4=coordsChange(x_world_S4,y_world,z_world_S4,numpy.pi/2)

#enemy
enemy = pygame.image.load('motorbike.png')
enemy_img=[enemy,enemy]
enemy_lanes=random.sample(range(1,3),2)
enemy_x1=360 + 40/3
enemy_x2=400
enemy_x3=400 + 80/3
enemy_y=411.025
enemyX=[]
enemyY=[]

#speed
speed=0
spped_from_angle=0.01
def speed_change(angle):
    """
    to convert the input angle into final speed 
    """
    final_speed = angle_to_accn_factor*angle
    return final_speed



#x,y,z to x,y function
def coordsChange(x_world,y_world,z_world,fov_angle):
    global xc,yc
    z_world=max(1,z_world)
    scaling_x=(x_res/2)/(numpy.tan(fov_angle/2))
    scaling_y=(y_res/2)/(numpy.tan(fov_angle/2))
    x_screen = x_res*.5*(1 + ((x_world-xc)/(numpy.tan(fov_angle/2)*z_world)))
    y_screen = y_res*.5*(1 - ((y_world-yc)/(numpy.tan(fov_angle/2)*z_world)))
    return x_screen,y_screen

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))


def main_game_execution():
    
    

    #FOR AAKASH SPEED WITH ANGLE
    '''speed_from_angle = speed_change(global_angle)'''

    for i in enemy_lanes:
        if i==1:
            enemyX.append(enemy_x1)
            enemyY.append(enemy_y)
        elif i==2:
            enemyX.append(enemy_x2)
            enemyY.append(enemy_y)
        elif i==3:
            enemyX.append(enemy_x2)
            enemyY.append(enemy_y)
        
    #game loop
    running=True
    while running:
        #RGB
        screen.fill((0,0,0))
        #drawing road
        pygame.draw.polygon(screen,(92,95,102),((x1,y1),(x2,y2),(x3,y3),(x4,y4)))
        #drawing sky
        pygame.draw.rect(screen,(135,206,235),(0,0,x_res,y1))
        #drawing grass
        pygame.draw.polygon(screen,(89,166,8),((0,y1),(x1,y2),(x4,y3),(0,y4)))
        pygame.draw.polygon(screen,(89,166,8),((x2,y1),(x_res,y2),(x_res,y3),(x3,y4)))
        #drawing stripes
        pygame.draw.polygon(screen,(255,255,255),((xs1,ys1),(xs2,ys2),(xs3,ys3),(xs4,ys4)))
        pygame.draw.polygon(screen,(255,255,255),((xS1,yS1),(xS2,yS2),(xS3,yS3),(xS4,yS4)))
        #moving stripes
        if(z_world_S3>=1):
            z_world_s1-=0.1
            z_world_s2-=0.1
            z_world_s3-=0.1
            z_world_s4-=0.1

            xs1,ys1=coordsChange(x_world_s1,y_world,z_world_s1,numpy.pi/2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            xs2,ys2=coordsChange(x_world_s2,y_world,z_world_s2,numpy.pi/2)
            xs3,ys3=coordsChange(x_world_s3,y_world,z_world_s3,numpy.pi/2)
            xs4,ys4=coordsChange(x_world_s4,y_world,z_world_s4,numpy.pi/2)

            z_world_S1-=0.1
            z_world_S2-=0.1
            z_world_S3-=0.1
            z_world_S4-=0.1

            xS1,yS1=coordsChange(x_world_S1,y_world,z_world_S1,numpy.pi/2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            xS2,yS2=coordsChange(x_world_S2,y_world,z_world_S2,numpy.pi/2)
            xS3,yS3=coordsChange(x_world_S3,y_world,z_world_S3,numpy.pi/2)
            xS4,yS4=coordsChange(x_world_S4,y_world,z_world_S4,numpy.pi/2)

        else:
            z_world_s1=18
            z_world_s2=18
            z_world_s3=20
            z_world_s4=20
            
            z_world_S1=18
            z_world_S2=18
            z_world_S3=20
            z_world_S4=20

            xs1,ys1=coordsChange(x_world_s1,y_world,z_world_s1,numpy.pi/2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            xs2,ys2=coordsChange(x_world_s2,y_world,z_world_s2,numpy.pi/2)
            xs3,ys3=coordsChange(x_world_s3,y_world,z_world_s3,numpy.pi/2)
            xs4,ys4=coordsChange(x_world_s4,y_world,z_world_s4,numpy.pi/2)


            xS1,yS1=coordsChange(x_world_S1,y_world,z_world_S1,numpy.pi/2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            xS2,yS2=coordsChange(x_world_S2,y_world,z_world_S2,numpy.pi/2)
            xS3,yS3=coordsChange(x_world_S3,y_world,z_world_S3,numpy.pi/2)
            xS4,yS4=coordsChange(x_world_S4,y_world,z_world_S4,numpy.pi/2)
        
        #background image
        #screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    speed = -speed_from_angle
                if event.key==pygame.K_RIGHT:
                    speed= speed_from_angle
                    
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    speed = 0
                    
        #camera change
        xc+=speed
        
        #road change
        if(speed!=0):
            x1,y1=coordsChange(x_world1,y_world,z_world1,numpy.pi/2)
            x2,y2=coordsChange(x_world2,y_world,z_world2,numpy.pi/2)
            x3,y3=coordsChange(x_world3,y_world,z_world3,numpy.pi/2)
            x4,y4=coordsChange(x_world4,y_world,z_world4,numpy.pi/2)

        #boundary
        if xc>=1.5:
            xc=1.5
        if xc<=-1.5:
            xc=-1.5

        #enemyloop
            for i in range(0,1):
                enemy(enemyX[i],enemyY[i],i)

        pygame.display.flip()
