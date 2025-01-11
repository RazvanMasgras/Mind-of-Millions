import pygame

# Initialize pygame
pygame.init()

# Screen settings
SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Mind of Millions")

# Load background image
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (1920, 1080))

# Load template image
template = pygame.image.load("template.png")
template = pygame.transform.scale(template, (1600, 206))

# Define button areas for the answers
button1 = pygame.Rect(335, 780, 615, 50)  # Adjust coordinates for 1920x1080
button2 = pygame.Rect(955, 780, 615, 50)
button3 = pygame.Rect(335, 835, 615, 50)
button4 = pygame.Rect(955, 835, 615, 50)

# Main game loop
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False  # Exit fullscreen with Escape
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Detect clicks on buttons
            if button1.collidepoint(event.pos):
                print("Button 1 clicked!")
            elif button2.collidepoint(event.pos):
                print("Button 2 clicked!")
            elif button3.collidepoint(event.pos):
                print("Button 3 clicked!")
            elif button4.collidepoint(event.pos):
                print("Button 4 clicked!")

    # Draw the background image
    SCREEN.blit(background, (0, 0))

    SCREEN.blit(template, (150, 680))

    # Update the screen
    pygame.display.flip()

# Quit pygame
pygame.quit()
