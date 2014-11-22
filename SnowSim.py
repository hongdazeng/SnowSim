# Import a library of functions called 'pygame'
import pygame
import random

# Initialize the game engine
pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

MyScreenLength = 1920
MyScreenWidth = 1080

DisplayHelp = True
PlayingMusic = True

# Set the height and width of the screen
SIZE = [400, 400]
SnowSize = 5

DY = 1
DX = 1

screen = pygame.display.set_mode((MyScreenLength, MyScreenWidth), pygame.FULLSCREEN)
pygame.display.set_caption("Snow Animation")

background_image = pygame.image.load("background.png").convert()
help_image = pygame.image.load("h2.png").convert()

pygame.mixer.music.load('silent.ogg')
pygame.mixer.music.play(0)
# Create an empty array
snow_list = []

for i in range(500):
    x = random.randrange(0, MyScreenLength)
    y = random.randrange(0, MyScreenWidth)
    snow_list.append([x, y])

clock = pygame.time.Clock()

# Loop until the user press q
done = False
while not done:

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_q]:
                done = True
            elif pygame.key.get_pressed()[pygame.K_UP]:
                for b in range(10):
                    x = random.randrange(0, MyScreenLength)
                    y = random.randrange(0, MyScreenWidth)
                    snow_list.append([x, y])
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                if len(snow_list) > 20:
                    for c in range(10):
                        snow_list.pop(random.randrange(len(snow_list)))
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if SnowSize > 1:
                    SnowSize -= 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                SnowSize += 1
            elif pygame.key.get_pressed()[pygame.K_h]:
                if DisplayHelp:
                    help_image = pygame.image.load("h2.png").convert()
                    DisplayHelp = False
                else:
                    help_image = pygame.image.load("h1.png").convert()
                    DisplayHelp = True
            elif pygame.key.get_pressed()[pygame.K_KP8]:
                DY += 1
            elif pygame.key.get_pressed()[pygame.K_KP2]:
                DY -= 1
            elif pygame.key.get_pressed()[pygame.K_KP6]:
                DX += 1
            elif pygame.key.get_pressed()[pygame.K_KP4]:
                DX -= 1
            elif pygame.key.get_pressed()[pygame.K_KP0]:
                DX = 1
                DY = 1
            elif pygame.key.get_pressed()[pygame.K_m]:
                if PlayingMusic:
                    pygame.mixer.pause()
                    PlayingMusic = False

                else:
                    pygame.mixer.unpause()
                    PlayingMusic = True


    screen.blit(background_image, [0, 0])
    screen.blit(help_image, [1500, 50])

    # Process each snow flake in the list
    for i in range(len(snow_list)):

        # Draw the snow flake
        pygame.draw.circle(screen, WHITE, snow_list[i], SnowSize)

        # Move the snow flake based on dx and dy
        snow_list[i][0] += DX
        snow_list[i][1] += DY

        # reset the snow if it completely left the screen
        if snow_list[i][1] > MyScreenWidth + SnowSize:
            # Reset it some distance above the top
            y = random.randrange(-1*SnowSize, 0*SnowSize)
            snow_list[i][1] = y
            # Give it a new x position
            x = random.randrange(0, MyScreenLength)
            snow_list[i][0] = x

        if snow_list[i][0] > MyScreenLength + SnowSize:
            # Reset it some distance from left
            x = random.randrange(-1*SnowSize, 0*SnowSize)
            snow_list[i][0] = x
            # Give it a new x position
            y = random.randrange(0, MyScreenWidth)
            snow_list[i][1] = y

        if snow_list[i][0] < 0 - SnowSize - 5:
            x = random.randrange(-10*SnowSize + MyScreenLength, -2*SnowSize + MyScreenLength)
            y = random.randrange(0, MyScreenWidth)
            snow_list[i][0] = x
            snow_list[i][1] = y

        if snow_list[i][1] < 0 - SnowSize - 5:
            y = random.randrange(-10*SnowSize + MyScreenWidth, -2*SnowSize + MyScreenWidth)
            x = random.randrange(0, MyScreenLength)
            snow_list[i][0] = x
            snow_list[i][1] = y

    # Yo update
    pygame.display.flip()
    clock.tick(60)