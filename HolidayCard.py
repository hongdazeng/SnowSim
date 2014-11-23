# Import a library of functions called 'pygame'
import pygame
import random
import os

"""
Purdue Computer Science Women's Network / Microsoft Hackathon Project
"""

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

myfont = pygame.font.SysFont("monospace", 150)
label1 = myfont.render("Merry", 1, (204, 22, 0))
label2 = myfont.render("Christmas!", 1, (204, 22, 0))

screen = pygame.display.set_mode((MyScreenLength, MyScreenWidth), pygame.FULLSCREEN)
pygame.display.set_caption("Snow Animation")

background = os.path.join('data', "background.png")
background_image = pygame.image.load(background).convert()
help2 = os.path.join('data', 'h2.png')
help_image = pygame.image.load(help2).convert()

soundName = fullname = os.path.join('data', 'silent.ogg')
pygame.mixer.music.load(soundName)
pygame.mixer.music.play(0)

help1 = os.path.join('data', 'h1.png')
# Create an empty array
Snow_List = []

for i in range(500):
    x = random.randrange(0, MyScreenLength)
    y = random.randrange(0, MyScreenWidth)
    Snow_List.append([x, y])

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
                    Snow_List.append([x, y])
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                if len(Snow_List) > 20:
                    for c in range(10):
                        Snow_List.pop(random.randrange(len(Snow_List)))
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if SnowSize > 1:
                    SnowSize -= 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                SnowSize += 1
            elif pygame.key.get_pressed()[pygame.K_h]:
                if DisplayHelp:
                    help_image = pygame.image.load(help2).convert()
                    DisplayHelp = False
                else:
                    help_image = pygame.image.load(help1).convert()
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
                    pygame.mixer.music.pause()
                    PlayingMusic = False

                else:
                    pygame.mixer.music.unpause()
                    PlayingMusic = True
            elif pygame.key.get_pressed()[pygame.K_RETURN]:
                d = random.randint(1, 5)
                if d == 1:
                    label1 = myfont.render("Merry", 1, (204, 22, 0))
                    label2 = myfont.render("Christmas!", 1, (204, 22, 0))
                if d == 2:
                    label1 = myfont.render("Happy", 1, (204, 22, 0))
                    label2 = myfont.render("New Year!", 1, (204, 22, 0))
                if d == 3:
                    label1 = myfont.render("Party", 1, (204, 22, 0))
                    label2 = myfont.render("Hard!", 1, (204, 22, 0))
                if d == 4:
                    label1 = myfont.render("Code", 1, (204, 22, 0))
                    label2 = myfont.render("On!", 1, (204, 22, 0))

    screen.blit(background_image, [0, 0])
    screen.blit(help_image, [1500, 50])

    # Process each snow flake in the list
    for i in range(len(Snow_List)):

        # Draw the snow flake
        pygame.draw.circle(screen, WHITE, Snow_List[i], SnowSize)

        # Move the snow flake based on dx and dy
        Snow_List[i][0] += DX
        Snow_List[i][1] += DY

        # reset the snow if it completely left the screen
        if Snow_List[i][1] > MyScreenWidth + SnowSize:
            # Reset it some distance above the top
            y = random.randrange(-1 * SnowSize, 0 * SnowSize)
            Snow_List[i][1] = y
            # Give it a new x position
            x = random.randrange(0, MyScreenLength)
            Snow_List[i][0] = x

        if Snow_List[i][0] > MyScreenLength + SnowSize:
            # Reset it some distance from left
            x = random.randrange(-1 * SnowSize, 0 * SnowSize)
            Snow_List[i][0] = x
            # Give it a new x position
            y = random.randrange(0, MyScreenWidth)
            Snow_List[i][1] = y

        if Snow_List[i][0] < 0 - SnowSize - 5:
            x = random.randrange(-10 * SnowSize + MyScreenLength, -2 * SnowSize + MyScreenLength)
            y = random.randrange(0, MyScreenWidth)
            Snow_List[i][0] = x
            Snow_List[i][1] = y

        if Snow_List[i][1] < 0 - SnowSize - 5:
            y = random.randrange(-10 * SnowSize + MyScreenWidth, -2 * SnowSize + MyScreenWidth)
            x = random.randrange(0, MyScreenLength)
            Snow_List[i][0] = x
            Snow_List[i][1] = y

    screen.blit(label1, (100, 100))
    screen.blit(label2, (250, 250))
    # Yo update
    pygame.display.flip()
    clock.tick(60)