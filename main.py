import pygame
import random
import button
import open_trivia_db

# Initialize pygame
pygame.init()

# Screen settings
SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Mind of Millions")

def loading_screen():
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))
    loading = pygame.image.load("loading.png")
    loading = pygame.transform.scale(loading, (1200, 800))
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(loading, (170, -50))
    pygame.display.flip()
    questions = open_trivia_db.gen_normal_mode()
    return play_menu()
    
def answer_clicked(button, is_correct):
    answer_surface = pygame.image.load("answer_button.png")
    answer_surface = pygame.transform.scale(answer_surface, (615, 50))
    waiting_surface = pygame.image.load("waiting_answer_button.png")
    waiting_surface = pygame.transform.scale(waiting_surface, (615, 50))
    correct_surface = pygame.image.load("correct_answer_button.png")
    correct_surface = pygame.transform.scale(correct_surface, (615, 50))
    incorrect_surface = pygame.image.load("wrong_answer_button.png")
    incorrect_surface = pygame.transform.scale(incorrect_surface, (615, 50))
    button.change_image(waiting_surface)
    button.update(SCREEN)
    pygame.display.flip()
    pygame.time.delay(1000)
    for _ in range(3):
        button.change_image(correct_surface if is_correct else incorrect_surface)
        button.update(SCREEN)
        pygame.display.flip()
        pygame.time.delay(200)
        button.change_image(answer_surface)
        button.update(SCREEN)
        pygame.display.flip()
        pygame.time.delay(200)
    button.change_image(correct_surface if is_correct else incorrect_surface)
    button.update(SCREEN)
    pygame.display.flip()
    pygame.time.delay(1800)
    button.change_image(answer_surface)
    button.update(SCREEN)
    pygame.display.flip()


def play_menu():
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))

    # Draw the background image
    SCREEN.blit(background, (0, 0))
    pygame.display.flip()

    # Load template image
    template = pygame.image.load("template.png")
    template = pygame.transform.scale(template, (1600, 206))

    answer_button_surface = pygame.image.load("answer_button.png")
    answer_button_surface = pygame.transform.scale(answer_button_surface, (615, 50))

    question_button_surface = pygame.image.load("question_button.png")
    question_button_surface = pygame.transform.scale(question_button_surface, (1000, 60))

    question_button = button.Button(question_button_surface, 950, 730, "This is a long ass fcuking question fuck razvan to test his mother on like rats like ballsac fuck ballsac in the ass asd ashdgqwhebqe qe qke kqe yiqwehg qwe biqweh oqweh iwb qwebqiwe iy", pygame.font.Font(None, 50))

    button1 = button.Button(answer_button_surface, 645, 805, "Answer 1", pygame.font.Font(None, 40))
    button2 = button.Button(answer_button_surface, 1260, 805, "Answer 2", pygame.font.Font(None, 40))
    button3 = button.Button(answer_button_surface, 645, 860, "Answer 3", pygame.font.Font(None, 40))
    button4 = button.Button(answer_button_surface, 1260, 860, "Answer 4", pygame.font.Font(None, 40))

    # Main game loop
    running = True
    while running:
        MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detect clicks on buttons
                if button1.check_for_input(MOUSE_POS):
                    answer_clicked(button1, True)
                elif button2.check_for_input(MOUSE_POS):
                    answer_clicked(button2, True)
                elif button3.check_for_input(MOUSE_POS):
                    answer_clicked(button3, False)
                elif button4.check_for_input(MOUSE_POS):
                    answer_clicked(button4, False)

        SCREEN.blit(template, (150, 680))
        # Update the buttons
        button1.update(SCREEN)
        button1.change_color(MOUSE_POS)
        button2.update(SCREEN)
        button2.change_color(MOUSE_POS)
        button3.update(SCREEN)
        button3.change_color(MOUSE_POS)
        button4.update(SCREEN)
        button4.change_color(MOUSE_POS)
        question_button.update(SCREEN)

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
                    return loading_screen()
                elif exit_button.check_for_input(MOUSE_POS):
                    pygame.quit()
    
        play_button.update(SCREEN)
        play_button.change_color(MOUSE_POS)
        exit_button.update(SCREEN)
        exit_button.change_color(MOUSE_POS)
        pygame.display.flip()

main_menu()
