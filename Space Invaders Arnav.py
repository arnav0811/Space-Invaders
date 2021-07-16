# Importing Modules
# Main Module - Pygame
import pygame
# Sub Module - Random - for randomness in enemy position
import random
# To find dist b/w enemy and bullet
import math
# For music
from pygame import mixer

# Initializing PyGame
pygame.init()

# Creating a screen (window)
screen = pygame.display.set_mode((780, 580))  # In pixels for window size - Coordinates

# Background Image
background = pygame.image.load('invaders.png')

# Background Sound
mixer.music.load('background.wav')  # Getting the music
mixer.music.play(-1)  # To play on loop

# Title and Icon for Pygame Window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship2.png")
pygame.display.set_icon(icon)

# Player Values in pixels
playerImg = pygame.image.load('spaceship2.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemies - put in lists such that it can be appended easily
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemynum = 6 # No.of enemies at any instance

# Loop to use same variables for multiple enemies
for i in range(enemynum):
    enemyImg.append(pygame.image.load('space-invader-icon.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(25)

# Bullet
bulletimage = pygame.image.load("bullet.png")
bulletX = 0  # X coordinate
bulletY = 480  # Y Coordinate
bulletX_change = 0  # Bullet won't move in X-Direction
bulletY_change = 10
bullet_state = "ready"  # state is whether the bullet is going to be firing or not

# Ready - Bullet is at rest - Cannot see it on screen
# Fire - Bullet in motion

# Score
# Calculating score of the user
score = 0

# Font to be displayed on the screen
font = pygame.font.Font("/Users/arnavmardia/Desktop/Space Invaders/space_invaders.ttf", 32)  # Getting the font

# X and Y Coordiantes for font
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font("space_invaders.ttf", 64)


# Function for displaying score
def show_score(x, y):
    # Rendering text on screen
    score_font = font.render("Score:" + str(score), True, (255, 152, 15))
    # Blit the score on screen
    screen.blit(score_font, (x, y))


def game_over_text():
    # Text for Game over
    over_text = over_font.render("GAME OVER", True, (255, 152, 15))
    # Blit game over text on screen
    screen.blit(over_text, (180, 240))


def level_two_text():
    level_text = over_font.render("LEVEL 2", True, (255, 152, 15))
    screen.blit(level_text, (480, 180))


# Function for Player
# Passing parameters x and y as coordinates to adjust the player location
def player(x, y):
    # Blit == Draw - drawing the image on the window after it loads
    screen.blit(playerImg, (x, y))


# Function for Enemy
# Passing parameters x and y as coordinates to adjust the player location
def enemy(x, y, i):
    # Blit == Draw - drawing the image on the window after it loads
    screen.blit(enemyImg[i], (x, y))


# Function to fire bullet
def fire_bullet(x, y):
    global bullet_state  # So that it can be used throughout
    bullet_state = "fire"
    screen.blit(bulletimage, (x + 16, y + 10))


# Function for collision b/w bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))

    if distance < 27:  # Pixels
        return True
    else:
        return False


level = 1

# GameLoop
running = True

# To quit the game / quit the game window
while running:  # Main running loop

    # Colour of Screen in RGB Values - Red, Green, Blue
    screen.fill((0, 1, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # checking all "events" that are running using for loop
        if event.type == pygame.QUIT:  # Exit function call
            running = False
            pygame.mixer.music.stop()
            print("GAME QUIT")
            print()

        # checking left/right keystroke
        if event.type == pygame.KEYDOWN:  # A key is pressed
            if event.key == pygame.K_LEFT:  # The Left Key is pressed
                print("Left arrow is pressed")
                print()
                playerX_change -= 3

            if event.key == pygame.K_RIGHT:  # The Right Key is pressed
                print("Right arrow is pressed")
                print()
                playerX_change += 3

            if event.key == pygame.K_SPACE:  # The Right Key is pressed
                if bullet_state is "ready":
                    # To get the sound of the bullet
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    # To get initial X Coordinate of space ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    print("Space bar has been pressed")
                    print()

        if event.type == pygame.KEYUP:  # Removal of key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # checking if either key is removed
                print("Keystroke has been released")
                print()
                playerX_change = 0

            elif event.key == pygame.K_SPACE:
                print("Keystroke has been released")
                print()

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Checking the boundary of player such that it doesn't go out of bounds
    playerX += playerX_change  # Updating coordinate of player on x axis

    if playerX <= 0:
        playerX = 0

    elif playerX >= 718:
        playerX = 718

    # Enemy Movement
    for i in range(enemynum):

        # Game Over
        if enemyY[i] > 430:
            # New for loop for all enemies
            for j in range(enemynum):
                # Taking all enemies out of the screen
                enemyY[j] = 2000

            # Calling game over function
            game_over_text()
            pygame.mixer.music.stop()
            break

        enemyX[i] += enemyX_change[i]  # Updating coordinate of enemy on x axis

        if enemyX[i] <= 0:
            enemyX_change[i] = 3  # After it hits the left boundary, increasing number of pixels to move back in
            enemyY[i] += enemyY_change[i]  # After it hits the boundary, moves downwards

        elif enemyX[i] >= 718:
            enemyX_change[i] = -3  # After it hits the right boundary, decreasing the number of pixels
            enemyY[i] += enemyY_change[i]

        # Collision
        collision1 = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision1:
            # Sound upon collision
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()

            # Position change upon collision
            bulletY = 480
            bullet_state = "ready"
            score += 10
            print(score)
            print("COLLISION!!")
            print()
            enemyX[i] = random.randint(0, 760)
            enemyY[i] = random.randint(50, 150)

        # Calling the enemy function
        enemy(enemyX[i], enemyY[i], i)  # Calling it after screen function as it needs to be above the screen layer

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling the player function so that it lasts throughout the game
    player(playerX, playerY)  # Calling it after screen function as it needs to be above the screen layer

    # Calling function to display score
    show_score(textX, textY)

    # Constantly Updating the display (Game Window)
    pygame.display.update()
