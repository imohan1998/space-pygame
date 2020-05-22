import pygame
import random
import math

pygame.init ( )
from pygame import mixer

screen = pygame.display.set_mode ((800, 600))

background = pygame.image.load ( 'background.png' )

mixer.music.load ( 'background.wav' )
m = mixer.music
m.play ( -1 )

pygame.display.set_caption ( "space hero mohan" )
icon = pygame.image.load ( 'alien.png' )
pygame.display.set_icon ( icon )

playerImg = pygame.image.load ( 'space-invaders.png' )
playerX = 370
playerY = 490
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range ( num_of_enemies ) :
    enemyImg.append ( pygame.image.load ( 'cartoon.png' ) )
    enemyX.append ( random.randint ( 0,735 ) )
    enemyY.append ( random.randint ( 50,150 ) )
    enemyX_change.append ( 2 )
    enemyY_change.append ( 40 )

bulletImg = pygame.image.load ( 'bullet.png' )
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

score_value = 0
font = pygame.font.Font ( 'freesansbold.ttf',32 )

textX = 10
textY = 10

over_font = pygame.font.Font ( 'freesansbold.ttf',64 )


def show_score(x,y) :
    score = font.render ( "score :" + str ( score_value ),True,(255,255,255) )
    screen.blit ( score,(x,y) )


def game_over_text() :
    over_text = font.render ( "GAME OVER",True,(255,255,255) )
    screen.blit ( over_text,(200,250) )


def player(X,Y) :
    screen.blit ( playerImg,(X,Y) )


def enemy(X,Y,i) :
    screen.blit ( enemyImg[i],(X,Y) )


def fire_bullet(X,Y) :
    global bullet_state
    bullet_state = "fire"
    screen.blit ( bulletImg,(X + 16,Y + 10) )
    # screen.blit ( bulletImg,(X ,Y ) )
    # screen.blit(bulletImg, (X + 32, Y +  20))


def isCollision(enemyX,enemyY,bulletX,bulletY) :
    distance = math.sqrt ( math.pow ( enemyX - bulletX,2 ) + math.pow ( enemyY - bulletY,2 ) )
    if distance < 27 :
        return True
    else :
        return False


running = True
while running :

    screen.fill ((2, 2, 50))
    screen.blit (background, (0, 0))
    for event in pygame.event.get ( ) :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                playerX_change = -2
            if event.key == pygame.K_RIGHT :
                playerX_change = 2
            if event.key == pygame.K_SPACE :
                if bullet_state == "ready" :
                    bullet_sound = mixer.Sound ( 'laser.wav' )
                    bullet_sound.play ( )
                    bulletX = playerX
                    fire_bullet ( playerX,bulletY )

        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736

    for i in range ( num_of_enemies ) :

        if enemyY[i] > 300 :
            for j in range ( num_of_enemies ) :
                enemyY[j] = 2000
            game_over_text ( )
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 :
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736 :
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

    for i in range ( num_of_enemies ) :
        collision = isCollision ( enemyX[i],enemyY[i],bulletX,bulletY )
        if collision :
            collision_sound = mixer.Sound ( 'explosion.wav' )
            collision_sound.play ( )
            bulletY = 400
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint (0, 735)
            enemyY[i] = random.randint (50, 150)

        enemy ( enemyX[i],enemyY[i],i )

    if bulletY <= 0 :
        bulletY = 490
        bullet_state = "ready"

    if bullet_state == "fire" :
        fire_bullet ( bulletX,bulletY )
        bulletY -= bulletY_change

    player ( playerX,playerY )
    show_score ( textX,textY )
    pygame.display.update ( )
