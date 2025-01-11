import pygame
import random
import button

# Initialize pygame
pygame.init()

# Screen settings
SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Mind of Millions")

def answer_clicked(template, correct_template, incorrect_template, waiting_template, is_correct):
    waiting_template = pygame.image.load(waiting_template)
    waiting_template = pygame.transform.scale(waiting_template, (1600, 206))
    new_template = pygame.image.load(correct_template if is_correct else incorrect_template)
    new_template = pygame.transform.scale(new_template, (1600, 206))
    SCREEN.blit(waiting_template, (150, 680))
    pygame.display.flip()
    pygame.time.delay(1000)
    for _ in range(3):
        SCREEN.blit(new_template, (150, 680))
        pygame.display.flip()
        pygame.time.delay(200)
        SCREEN.blit(template, (150, 680))
        pygame.display.flip()
        pygame.time.delay(200)
    SCREEN.blit(new_template, (150, 680))
    pygame.display.flip()
    pygame.time.delay(1800)


def play_menu():

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
                return main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detect clicks on buttons
                if button1.collidepoint(event.pos):
                    is_correct = random.randint(1, 10) > 5
                    answer_clicked(template, "template_correct_1.png", "template_incorrect_1.png", "template_waiting_1.png", is_correct)
                elif button2.collidepoint(event.pos):
                    is_correct = random.randint(1, 10) > 5
                    answer_clicked(template, "template_correct_2.png", "template_incorrect_2.png", "template_waiting_2.png", is_correct)
                elif button3.collidepoint(event.pos):
                    is_correct = random.randint(1, 10) > 5
                    answer_clicked(template, "template_correct_3.png", "template_incorrect_3.png", "template_waiting_3.png", is_correct)
                elif button4.collidepoint(event.pos):
                    is_correct = random.randint(1, 10) > 5
                    answer_clicked(template, "template_correct_4.png", "template_incorrect_4.png", "template_waiting_4.png", is_correct)

        # Draw the background image
        SCREEN.blit(background, (0, 0))

        # Draw the template on the screen (centered)
        SCREEN.blit(template, (150, 680))

        # Update the screen
        pygame.display.flip()

def main_menu():

    button_surface = pygame.image.load("button.png")
    button_surface = pygame.transform.scale(button_surface, (530, 100))

    play_button = button.Button(button_surface, 960, 740, "PLAY", pygame.font.Font(None, 50))
    exit_button = button.Button(button_surface, 960, 850, "EXIT", pygame.font.Font(None, 50))

    background = pygame.image.load("main_menu_bg.webp")
    background = pygame.transform.scale(background, (1920, 1080))

    title = pygame.image.load("title.png")
    title = pygame.transform.scale(title, (2000, 1000))

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(title, (-30, 150))
    pygame.display.flip()

    running = True
    while running: 
        MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit pygame
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Exit fullscreen with Escape
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return play_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(MOUSE_POS):
                    return play_menu()
                elif exit_button.check_for_input(MOUSE_POS):
                    pygame.quit()
    
        play_button.update(SCREEN)
        play_button.change_color(MOUSE_POS)
        exit_button.update(SCREEN)
        exit_button.change_color(MOUSE_POS)
        pygame.display.flip()

main_menu()
