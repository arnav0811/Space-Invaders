# Importing python game library
import pygame as pyg

# Importing python random library
import random

# Importing python math library
import math 

# For music
from pygame import mixer


# Initialize pygame
pyg.init()

# setting up screen
# width,height of screen
# Width and height in pixels

screen = pyg.display.set_mode((780, 580))

# Background Theme and Sound

background = pyg.image.load('/Users/arnavmardia/Desktop/invaders.png')


# Title and Icon

pyg.display.set_caption("Space Invaders")
icon = pyg.image.load('/Users/arnavmardia/Desktop/Space Invaders/spaceship2.png')
pyg.display.set_icon(icon)

# Spaceship - Player

playerimage= pyg.image.load("/Users/arnavmardia/Desktop/Space Invaders/spaceship2.png")

# To determine location in the start

PlayerX = 355  # X coordinate
PlayerY = 485  # Y Coordinate
PlayerX_change = 0

# Enemy - Invader
# Creating multiple invaders using lists

enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemynum = 6

for a in range(enemynum):

    enemyimage.append(pyg.image.load("/Users/arnavmardia/Desktop/Space Invaders/space-invader-icon.png"))
    enemyX.append(random.randint(0, 716))   # X coordinate
    enemyY.append(random.randint(40, 230))  # Y Coordinate
    enemyX_change.append(8)
    enemyY_change.append(30)

# Bullet

bulletimage = pyg.image.load("/Users/arnavmardia/Desktop/Space Invaders/bullet.png" )
bulletX = 0    # X coordinate
bulletY = 460  # Y Coordinate
bulletX_change = 0
bulletY_change = 40
bullet_state = "Ready"

# Ready - Bullet is at rest
# Fire - Bullet in motion

# Score

score_value = 0

# Getting the font

font = pyg.font.Font("space_invaders.ttf", 32)  # Font - CHANGE FONT

# X and Y Coordiante of font

textX = 10
textY = 10

# Game Over text

over_font = pyg.font.Font("space_invaders.ttf", 64)

# Defining a function to display the score

def show_score(x,y):
    # Rendering the text with its colour and font type

    score = font.render("Score:" + str(score_value), True, (255, 152, 15))
    screen.blit(score, (x, y))

# Defining a function for game over text

def game_over_text():

    over_text = over_font.render("GAME OVER", True, (255, 152, 15))
    screen.blit(over_text, (180, 230))

# Defining a function for spaceship(player)

def player(x,y):

    # Drawing the image of player on screen with coordinates

    screen.blit(playerimage, (x, y))

# Defining a function for enemy(invader)

def enemy(x,y,a):

    # Drawing the image of enemy on screen with coordinates

    screen.blit(enemyimage[a], (x,y))

# Defining a function when bullet is fired

def fire_bullet(x,y):

    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimage,(x+10, y+10))   # x+16, y+10 ---> To keep it in the centre


def Collision(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY -  bulletY, 2)))

    if distance < 27:
        return True
    else:
        return False

# Game Loop

run = True
while run:

    # Red, Green, Blue - Colour of Screen (RGB)

    screen.fill((0, 1, 0))

    # For background image

    screen.blit(background, (0, 0))

    for event in pyg.event.get():

        if event.type == pyg.QUIT:       # Infinite Loop but does not affect unless we quit pygame.
            run = False

        # if keystroke is pressed check whether movement has to be left or right

        if event.type == pyg.KEYDOWN:

            if event.key == pyg.K_LEFT:
                PlayerX_change = -10  # Movement towards left when left arrow is clicked


            if event.key == pyg.K_RIGHT:
                PlayerX_change = 10   # Movement towards right when right arrow is clicked


            if event.key == pyg.K_SPACE:

                if bullet_state == "Ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # So that the bullet position does not follow the spaceship movement
                    bulletX = PlayerX
                    fire_bullet(PlayerX, bulletY)

        if event.type == pyg.KEYUP:

            if event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:

                # Release of keystroke - no change in position

                PlayerX_change = 0



    PlayerX += PlayerX_change

    # X-coordinate of spaceship movement

    if PlayerX <= 0:
        PlayerX = 0

    elif PlayerX >= (716):
        # Subtracting 64 because image size is 64x64
        PlayerX = 716

    # Enemy Movement

    for a in range(enemynum):

        # GAME OVER

        if enemyY[a] > 440:

            for b in range(enemynum):        # To stop the game when any one enemy hits the spaceship
                enemyY[b] = 2000             # Removing all the invaders from the screen
            game_over_text()                 # Showing game over text
            break

        enemyX[a] += enemyX_change[a]        # Using list index function to specify which element of the list needs to be altered
        if enemyX[a] <= 0:

            enemyX_change[a] = 10
            enemyY[a] += enemyY_change[a]

        elif enemyX[a] >= 716:

            enemyX_change[a] = -10           # Subtracting because image size is 64x64
            enemyY[a] += enemyY_change[a]

        # Collision
        # Calling function collision

        collision1 = Collision(enemyX[a], enemyY[a], bulletX, bulletY)

        if collision1:

            explosion_sound = mixer.Sound("/Users/arnavmardia/Desktop/Space Invaders/explosion.wav")
            explosion_sound.play()
            bulletY = 480                   # Reset the bullet to starting point after collision
            bullet_state = "Ready"          # Change its state after collision

            score_value += 10               # Increasing score after every collision

            enemyX[a] = random.randint(0, (580 - 64))  # Re-spawn to a random x-coordinate after collision
            enemyY[a] = random.randint(40, 230)        # Re-spawn to a random y-coordinate after collision

        enemy(enemyX[a], enemyY[a], a)

    # Bullet Movement

    if bulletY < 0:
        bulletY = 460                                  # To reset the bullet at original position after shooting
        bullet_state = "Ready"

    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    # Calling function in loop such that it stays on screen

    player(PlayerX, PlayerY)

    # Calling function of text to display the score

    show_score(textX, textY)

    # Calling enemy function such that it stays on screen

    pyg.display.update()





