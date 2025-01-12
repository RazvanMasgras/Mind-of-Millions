import pygame
import random
import button
import open_trivia_db


PRIZES = (0,
          100, 
          200, 
          300, 
          500, 
          1000, 
          2000, 
          4000, 
          8000, 
          16000, 
          32000, 
          64000,
          125000,
          250000,
          500000,
          1000000)
TEXT_BOX = (400, 680, 1100, 90)

# Initialize pygame
pygame.init()
pygame.mixer.init()
wrong_answer = pygame.mixer.Sound("wrong_answer.mp3")
correct_answer = pygame.mixer.Sound("correct_answer.mp3")
final_answer = pygame.mixer.Sound("final_answer.mp3")

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
    return play_menu(questions)
    
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
    final_answer.play().fadeout(2500)
    pygame.time.delay(2500)
    if not is_correct:
        wrong_answer.play().fadeout(3000)
    else:
        correct_answer.play().fadeout(3000)
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

def display_next_question(question, button1, button2, button3, button4):
    answers = question["answers"]
    button1.change_text(answers[0])
    button2.change_text(answers[1])
    button3.change_text(answers[2])
    button4.change_text(answers[3])
    button1.update(SCREEN)
    button2.update(SCREEN)
    button3.update(SCREEN)
    button4.update(SCREEN)
    pygame.display.flip()

def display_text(text, font, color, position):
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, position)
    pygame.display.flip()

def display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button):
    fifty_fifty_button.update(SCREEN)
    phone_a_friend_button.update(SCREEN)
    audience_poll_button.update(SCREEN)
    pygame.display.flip()

def play_menu(questions):
    # Load background image
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))

    # Load template image
    template = pygame.image.load("template.png")
    template = pygame.transform.scale(template, (1600, 206))

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(template, (150, 680))
    pygame.display.flip()

    current_question = 0
    question = questions[current_question]
    answers = question["answers"]

    answer_button_surface = pygame.image.load("answer_button.png")
    answer_button_surface = pygame.transform.scale(answer_button_surface, (615, 50))

    button1 = button.Button(answer_button_surface, 645, 805, answers[0], pygame.font.Font(None, 40))
    button2 = button.Button(answer_button_surface, 1260, 805, answers[1], pygame.font.Font(None, 40))
    button3 = button.Button(answer_button_surface, 645, 860, answers[2], pygame.font.Font(None, 40))
    button4 = button.Button(answer_button_surface, 1260, 860, answers[3], pygame.font.Font(None, 40))

    fifty_fifty_surface = pygame.image.load("fifty-fifty.png")
    fifty_fifty_surface = pygame.transform.scale(fifty_fifty_surface, (100, 100))
    phone_a_friend_surface = pygame.image.load("phone-a-friend.png")
    phone_a_friend_surface = pygame.transform.scale(phone_a_friend_surface, (100, 100))
    audience_poll_surface = pygame.image.load("ask-the-audience.png")
    audience_poll_surface = pygame.transform.scale(audience_poll_surface, (100, 100))

    fifty_fifty_button = button.Button(fifty_fifty_surface, 400, 200, "", pygame.font.Font(None, 50))
    phone_a_friend_button = button.Button(phone_a_friend_surface, 500, 200, "", pygame.font.Font(None, 50))
    audience_poll_button = button.Button(audience_poll_surface, 600, 200, "", pygame.font.Font(None, 50))

    fifty_fifty_button.update(SCREEN)
    phone_a_friend_button.update(SCREEN)
    audience_poll_button.update(SCREEN)
    pygame.display.flip()

    display_next_question(question, button1, button2, button3, button4)

    display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
    display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))

    # Main game loop
    running = True
    while running:
        button.render_text_box(SCREEN, question["question"], TEXT_BOX)
        pygame.display.flip()

        for event in pygame.event.get():
            MOUSE_POS = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detect clicks on buttons
                print(questions[current_question]["correct_answer"])
                if button1.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[0])
                    answer_clicked(button1, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14:
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                        display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else :
                        pygame.event.clear()
                        return lose_screen()
                elif button2.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[1])
                    answer_clicked(button2, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14:
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                        display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else:
                        pygame.event.clear()
                        return lose_screen()
                elif button3.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[2])
                    answer_clicked(button3, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14:
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                        display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else :
                        pygame.event.clear()
                        return lose_screen()
                elif button4.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[3])
                    answer_clicked(button4, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14:
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                        display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else :
                        pygame.event.clear()
                        return lose_screen()
                elif fifty_fifty_button.check_for_input(MOUSE_POS) and not fifty_fifty_button.used:
                    fifty_fifty_button.used = True
                    used_surface = pygame.image.load("used_fifty-fifty.png")
                    used_surface = pygame.transform.scale(used_surface, (100, 100))
                    fifty_fifty_button.change_image(used_surface)
                    question = open_trivia_db.fifty_fifty(question)
                    for i, b in enumerate([button1, button2, button3, button4]):
                        b.change_text(question["answers"][i])
                        b.update(SCREEN)
                        pygame.display.flip()
                    pygame.event.clear()
                elif phone_a_friend_button.check_for_input(MOUSE_POS) and not phone_a_friend_button.used:
                    phone_a_friend_button.used = True
                    used_surface = pygame.image.load("used_phone-a-friend.png")
                    used_surface = pygame.transform.scale(used_surface, (100, 100))
                    phone_a_friend_button.change_image(used_surface)
                    display_text("Your friend says: " + open_trivia_db.phone_a_friend(question), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 200))
                    pygame.event.clear()
                elif audience_poll_button.check_for_input(MOUSE_POS) and not audience_poll_button.used:
                    audience_poll_button.used = True
                    used_surface = pygame.image.load("used_ask-the-audience.png")
                    used_surface = pygame.transform.scale(used_surface, (100, 100))
                    audience_poll_button.change_image(used_surface)
                    weights = open_trivia_db.audience_poll(question)
                    display_text("Audience poll results:", pygame.font.Font("freesansbold.ttf", 50), "white", (750, 200))
                    for answer, weight in weights.items():
                        display_text(answer + ": " + str(weight) + "%", pygame.font.Font("freesansbold.ttf", 50), "white", (750, 250 + list(weights.keys()).index(answer) * 50))
                    pygame.event.clear()

def win_screen():
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))
    win = pygame.image.load("win.png")
    win = pygame.transform.scale(win, (1500, 1000))
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(win, (210, 70))
    pygame.display.flip()
    button_surface = pygame.image.load("exit_button.webp")
    button_surface = pygame.transform.scale(button_surface, (530, 150))
    back_button = button.Button(button_surface, 960, 840, "Back to main menu", pygame.font.Font(None, 50))
    back_button.update(SCREEN)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    pygame.event.clear()
                    return main_menu()   

def lose_screen():
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))
    lose = pygame.image.load("lost.png")
    lose = pygame.transform.scale(lose, (1200, 500))
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(lose, (390, 180))
    pygame.display.flip()
    button_surface = pygame.image.load("exit_button.webp")
    button_surface = pygame.transform.scale(button_surface, (530, 150))
    retry_button = button.Button(button_surface, 960, 710, "Try again", pygame.font.Font(None, 50))
    back_button = button.Button(button_surface, 960, 810, "Back to main menu", pygame.font.Font(None, 50))
    retry_button.update(SCREEN)
    back_button.update(SCREEN)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    pygame.event.clear()
                    return main_menu()
                elif retry_button.check_for_input(pygame.mouse.get_pos()):
                    pygame.event.clear()
                    return loading_screen()

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

        for event in pygame.event.get():
            MOUSE_POS = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                # Quit pygame
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Exit fullscreen with Escape
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(MOUSE_POS):
                    pygame.event.clear()
                    return loading_screen()
                elif exit_button.check_for_input(MOUSE_POS):
                    pygame.event.clear()
                    pygame.quit()
    
        play_button.update(SCREEN)
        play_button.change_color(pygame.mouse.get_pos())
        exit_button.update(SCREEN)
        exit_button.change_color(pygame.mouse.get_pos())
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
