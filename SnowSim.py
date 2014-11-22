# Import a library of functions called 'pygame'
import pygame
import random

# Initialize the game engine
pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

MyScreenLength = 1920
MyScreenWidth = 1080

# Set the height and width of the screen
SIZE = [400, 400]
SnowSize = 5

screen = pygame.display.set_mode((MyScreenLength, MyScreenWidth), pygame.FULLSCREEN)
pygame.display.set_caption("Snow Animation")

background_image = pygame.image.load("background.png").convert()
# Create an empty array
snow_list = []

# Loop 50 times and add a snow flake in a random x,y position
for i in range(100):
    x = random.randrange(0, MyScreenLength)
    y = random.randrange(0, MyScreenWidth)
    snow_list.append([x, y])

clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
while not done:

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP]:
                x = random.randrange(0, MyScreenLength)
                y = random.randrange(0, MyScreenWidth)
                snow_list.append([x, y])
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                snow_list.pop(random.randrange(len(snow_list)))
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if SnowSize > 1:
                    SnowSize -= 1
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                SnowSize += 1

    # Set the screen background
    # screen.fill(BLACK)
    screen.blit(background_image, [0, 0])

    # Process each snow flake in the list
    for i in range(len(snow_list)):

        # Draw the snow flake
        pygame.draw.circle(screen, WHITE, snow_list[i], SnowSize)

        # Move the snow flake down one pixel
        snow_list[i][1] += 1

        # reset the snow if complete left the screen
        if snow_list[i][1] > MyScreenWidth + SnowSize:
            # Reset it just above the top
            y = random.randrange(-10*SnowSize, -2*SnowSize)
            snow_list[i][1] = y
            # Give it a new x position
            x = random.randrange(0, MyScreenLength)
            snow_list[i][0] = x

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    clock.tick(20)