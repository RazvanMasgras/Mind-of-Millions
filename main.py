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
wrong_answer = pygame.mixer.Sound("audio/wrong_answer.mp3")
correct_answer = pygame.mixer.Sound("audio/correct_answer.mp3")
final_answer = pygame.mixer.Sound("audio/final_answer.mp3")
question_sound = pygame.mixer.Sound("audio/question_sound.mp3")

# Screen settings
SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Mind of Millions")


def loading_screen(mode, categories=None, difficulty=None):
    """
    Displays a loading screen with background music and image, and generates questions based on the selected mode.
    Args:
        mode (str): The game mode, either "classic" or "endless".
        categories (list, optional): A list of categories for the endless mode. Defaults to None.
        difficulty (str, optional): The difficulty level for the endless mode. Defaults to None.
    Returns:
        list: A list of questions generated based on the selected mode.
    """
    pygame.mixer.music.load("audio/main_menu_song.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))
    loading = pygame.image.load("assets/loading.png")
    loading = pygame.transform.scale(loading, (1200, 800))
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(loading, (170, -50))
    pygame.display.flip()
    
    if mode == "classic":
        questions = open_trivia_db.gen_normal_mode()
    elif mode == "endless":
        if len(categories) == 0:
            questions = open_trivia_db.gen_endless_mode(difficulty=difficulty)
        else:
            questions = open_trivia_db.gen_endless_mode(categories, difficulty)
    pygame.mixer.music.stop()
    return play_menu(questions, mode)
    
def answer_clicked(button, is_correct):
    """
    Handles the visual and audio feedback when an answer button is clicked.

    Args:
        button (Button): The button that was clicked.
        is_correct (bool): Indicates whether the clicked answer is correct.

    This function performs the following steps:
    1. Loads and scales the images for different button states (answer, waiting, correct, incorrect).
    2. Changes the button image to the waiting state and updates the display.
    3. Plays the final answer sound and waits for 2.5 seconds.
    4. Plays the correct or wrong answer sound based on the `is_correct` flag.
    5. Flashes the button image between the correct/incorrect state and the original state three times.
    6. Changes the button image to the final correct/incorrect state and waits for 1.8 seconds.
    7. Resets the button image to the original state.
    """
    answer_surface = pygame.image.load("assets/answer_button.png")
    answer_surface = pygame.transform.scale(answer_surface, (615, 50))
    waiting_surface = pygame.image.load("assets/waiting_answer_button.png")
    waiting_surface = pygame.transform.scale(waiting_surface, (615, 50))
    correct_surface = pygame.image.load("assets/correct_answer_button.png")
    correct_surface = pygame.transform.scale(correct_surface, (615, 50))
    incorrect_surface = pygame.image.load("assets/wrong_answer_button.png")
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
    """
    Updates the display with the next question and its corresponding answer buttons.

    Args:
        question (dict): A dictionary containing the question and its answers.
                         Expected to have a key "answers" with a list of answer strings.
        button1 (Button): The first answer button to be updated.
        button2 (Button): The second answer button to be updated.
        button3 (Button): The third answer button to be updated.
        button4 (Button): The fourth answer button to be updated.

    Returns:
        None
    """
    question_sound.play().fadeout(4500)
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
    """
    Renders and displays text on the screen at a specified position.

    Args:
        text (str): The text to be displayed.
        font (pygame.font.Font): The font object used to render the text.
        color (tuple): The color of the text in RGB format.
        position (tuple): The (x, y) coordinates where the text will be displayed on the screen.

    Returns:
        None
    """
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, position)
    pygame.display.flip()

def display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button):
    """
    Updates the display for the lifeline buttons and refreshes the screen.

    Args:
        fifty_fifty_button: The button object for the 50/50 lifeline.
        phone_a_friend_button: The button object for the Phone a Friend lifeline.
        audience_poll_button: The button object for the Audience Poll lifeline.
    """
    fifty_fifty_button.update(SCREEN)
    phone_a_friend_button.update(SCREEN)
    audience_poll_button.update(SCREEN)
    pygame.display.flip()

def play_menu(questions, mode):
    # Load background image
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))

    # Load template image
    template = pygame.image.load("assets/template.png")
    template = pygame.transform.scale(template, (1600, 206))

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(template, (150, 680))
    pygame.display.flip()

    current_question = 0
    question = questions[current_question]
    answers = question["answers"]

    answer_button_surface = pygame.image.load("assets/answer_button.png")
    answer_button_surface = pygame.transform.scale(answer_button_surface, (615, 50))

    button1 = button.Button(answer_button_surface, 645, 805, answers[0], pygame.font.Font(None, 40))
    button2 = button.Button(answer_button_surface, 1260, 805, answers[1], pygame.font.Font(None, 40))
    button3 = button.Button(answer_button_surface, 645, 860, answers[2], pygame.font.Font(None, 40))
    button4 = button.Button(answer_button_surface, 1260, 860, answers[3], pygame.font.Font(None, 40))

    fifty_fifty_surface = pygame.image.load("assets/fifty-fifty.png")
    fifty_fifty_surface = pygame.transform.scale(fifty_fifty_surface, (100, 100))
    phone_a_friend_surface = pygame.image.load("assets/phone-a-friend.png")
    phone_a_friend_surface = pygame.transform.scale(phone_a_friend_surface, (100, 100))
    audience_poll_surface = pygame.image.load("assets/ask-the-audience.png")
    audience_poll_surface = pygame.transform.scale(audience_poll_surface, (100, 100))

    fifty_fifty_button = button.Button(fifty_fifty_surface, 400, 200, "", pygame.font.Font(None, 50))
    phone_a_friend_button = button.Button(phone_a_friend_surface, 500, 200, "", pygame.font.Font(None, 50))
    audience_poll_button = button.Button(audience_poll_surface, 600, 200, "", pygame.font.Font(None, 50))

    fifty_fifty_button.update(SCREEN)
    phone_a_friend_button.update(SCREEN)
    audience_poll_button.update(SCREEN)
    pygame.display.flip()

    display_next_question(question, button1, button2, button3, button4)

    if mode == "classic":
        display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
        display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
    else :
        display_text("Score : " + str(current_question * 100), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))


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
                pygame.event.clear()
                return main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detect clicks on buttons
                print(questions[current_question]["correct_answer"])
                if button1.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[0])
                    answer_clicked(button1, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14 and mode == "classic":
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        if mode == "classic":
                            display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                            display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        else:
                            display_text("Score : " + str(current_question * 100), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else :
                        pygame.event.clear()
                        return lose_screen(mode)
                elif button2.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[1])
                    answer_clicked(button2, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14 and mode == "classic":
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        if mode == "classic":
                            display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                            display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        else:
                            display_text("Score : " + str(current_question * 100), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else:
                        pygame.event.clear()
                        return lose_screen(mode)
                elif button3.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[2])
                    answer_clicked(button3, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14 and mode == "classic":
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        if mode == "classic":
                            display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                            display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        else:
                            display_text("Score : " + str(current_question * 100), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else :
                        pygame.event.clear()
                        return lose_screen(mode)
                elif button4.check_for_input(MOUSE_POS):
                    is_correct = open_trivia_db.correct_answer(question, answers[3])
                    answer_clicked(button4, is_correct)
                    if is_correct:
                        current_question += 1
                        if current_question > 14 and mode == "classic":
                            return win_screen()
                        question = questions[current_question]
                        answers = question["answers"]
                        SCREEN.blit(background, (0, 0))
                        SCREEN.blit(template, (150, 680))
                        pygame.display.flip()
                        display_next_question(question, button1, button2, button3, button4)
                        if mode == "classic":
                            display_text("Current prize: $" + str(PRIZES[current_question]), pygame.font.Font("freesansbold.ttf", 50), "white", (750, 80))
                            display_text("Next win: $" + str(PRIZES[current_question + 1]), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        else:
                            display_text("Score : " + str(current_question * 100), pygame.font.Font("freesansbold.ttf", 70), "white", (750, 130))
                        display_lifelines(fifty_fifty_button, phone_a_friend_button, audience_poll_button)
                        pygame.event.clear()
                    else :
                        pygame.event.clear()
                        return lose_screen(mode)
                elif fifty_fifty_button.check_for_input(MOUSE_POS) and not fifty_fifty_button.used:
                    fifty_fifty_button.used = True
                    used_surface = pygame.image.load("assets/used_fifty-fifty.png")
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
                    used_surface = pygame.image.load("assets/used_phone-a-friend.png")
                    used_surface = pygame.transform.scale(used_surface, (100, 100))
                    phone_a_friend_button.change_image(used_surface)
                    button.render_text_box(SCREEN, "Your friend says the correct answer is: ", (450, 530, 1000, 100))
                    button.render_text_box(SCREEN, open_trivia_db.phone_a_friend(question), (450, 580, 1000, 100))
                    pygame.event.clear()
                elif audience_poll_button.check_for_input(MOUSE_POS) and not audience_poll_button.used:
                    audience_poll_button.used = True
                    used_surface = pygame.image.load("assets/used_ask-the-audience.png")
                    used_surface = pygame.transform.scale(used_surface, (100, 100))
                    audience_poll_button.change_image(used_surface)
                    
                    weights = open_trivia_db.audience_poll(question)
                    variants = ("A", "B", "C", "D")
                    display_text("Audience poll results:", pygame.font.Font("freesansbold.ttf", 30), "white", (350, 260))
                    for i in range(4):
                        pygame.draw.rect(SCREEN, (136, 6, 206), (375 + i * 70, 500 - weights[question["answers"][i]] * 2, 50, weights[question["answers"][i]] * 2))
                        display_text(variants[i], pygame.font.Font("freesansbold.ttf", 30), "white", (390 + i * 70, 515))

                    pygame.display.flip()
                    pygame.event.clear()
                    

def win_screen():
    pygame.mixer.music.load("audio/win_song.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))
    win = pygame.image.load("assets/win.png")
    win = pygame.transform.scale(win, (1500, 1000))
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(win, (210, 70))
    pygame.display.flip()
    button_surface = pygame.image.load("assets/exit_button.webp")
    button_surface = pygame.transform.scale(button_surface, (530, 150))
    back_button = button.Button(button_surface, 960, 840, "Back to main menu", pygame.font.Font(None, 50))
    back_button.update(SCREEN)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    pygame.mixer.music.stop()
                    pygame.event.clear()
                    return main_menu()   

def choose_game_mode_screen():
    background = pygame.image.load("assets/main_menu_bg.webp")
    background = pygame.transform.scale(background, (1920, 1080))
    SCREEN.blit(background, (0, 0))

    display_text("Choose difficulty:", pygame.font.Font(None, 75), "white", (740, 100))
    display_text("Choose categories:", pygame.font.Font(None, 75), "white", (730, 300))
    
    button_surface = pygame.image.load("assets/button.png")
    button_surface = pygame.transform.scale(button_surface, (450, 100))

    play_button = button.Button(button_surface, 960, 770, "PLAY", pygame.font.Font(None, 50))
    back_button = button.Button(button_surface, 960, 890, "BACK TO MAIN MENU", pygame.font.Font(None, 50))

    easy_button = button.Button(button_surface, 460, 220, "EASY", pygame.font.Font(None, 50))
    normal_button = button.Button(button_surface, 960, 220, "NORMAL", pygame.font.Font(None, 50))
    hard_button = button.Button(button_surface, 1460, 220, "HARD", pygame.font.Font(None, 50))


    history_button = button.Button(button_surface, 460, 420, "History", pygame.font.Font(None, 50))
    geography_button = button.Button(button_surface, 960, 420, "Geography", pygame.font.Font(None, 50))
    computer_science_button = button.Button(button_surface, 1460, 420, "Computer Science", pygame.font.Font(None, 50))
    sports_button = button.Button(button_surface, 460, 540, "Sports", pygame.font.Font(None, 50))
    vehicles_button = button.Button(button_surface, 960, 540, "Vehicles", pygame.font.Font(None, 50))
    music_button = button.Button(button_surface, 1460, 540, "Music", pygame.font.Font(None, 50))

    history_button.update(SCREEN)
    geography_button.update(SCREEN)
    computer_science_button.update(SCREEN)
    sports_button.update(SCREEN)
    vehicles_button.update(SCREEN)
    music_button.update(SCREEN)
    easy_button.update(SCREEN)
    normal_button.update(SCREEN)
    hard_button.update(SCREEN)
    back_button.update(SCREEN)
    play_button.update(SCREEN)
    pygame.display.flip()

    difficulty = ""
    categories = []

    running = True
    while running:
        for event in pygame.event.get():
            MOUSE_POS = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(MOUSE_POS):
                    pygame.event.clear()
                    return main_menu()
                elif play_button.check_for_input(MOUSE_POS):
                    return loading_screen("endless", categories, difficulty)
                elif easy_button.check_for_input(MOUSE_POS) and not easy_button.used:
                    difficulty = "easy"
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    normal_button.used = False
                    normal_button.change_image(button_surface)
                    hard_button.used = False
                    hard_button.change_image(button_surface)
                    easy_button.used = True
                    easy_button.change_image(used_surface)
                    easy_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif normal_button.check_for_input(MOUSE_POS) and not normal_button.used:
                    difficulty = "medium"
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    easy_button.used = False
                    easy_button.change_image(button_surface)
                    hard_button.used = False
                    hard_button.change_image(button_surface)
                    normal_button.used = True
                    normal_button.change_image(used_surface)
                    normal_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif hard_button.check_for_input(MOUSE_POS) and not hard_button.used:
                    difficulty = "hard"
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    easy_button.used = False
                    easy_button.change_image(button_surface)
                    normal_button.used = False
                    normal_button.change_image(button_surface)
                    hard_button.used = True
                    hard_button.change_image(used_surface)
                    hard_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif history_button.check_for_input(MOUSE_POS):
                    if (history_button.used):
                        categories.remove(history_button.text_input)
                    else:
                        categories.append(history_button.text_input)
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    history_button.used = not history_button.used
                    history_button.change_image(used_surface if history_button.used else button_surface)
                    history_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif geography_button.check_for_input(MOUSE_POS):
                    if (geography_button.used):
                        categories.remove(geography_button.text_input)
                    else:
                        categories.append(geography_button.text_input)
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    geography_button.used = not geography_button.used
                    geography_button.change_image(used_surface if geography_button.used else button_surface)
                    geography_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif computer_science_button.check_for_input(MOUSE_POS):
                    if (computer_science_button.used):
                        categories.remove(computer_science_button.text_input)
                    else:
                        categories.append(computer_science_button.text_input)
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    computer_science_button.used = not computer_science_button.used
                    computer_science_button.change_image(used_surface if computer_science_button.used else button_surface)
                    computer_science_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif sports_button.check_for_input(MOUSE_POS):
                    if (sports_button.used):
                        categories.remove(sports_button.text_input)
                    else:
                        categories.append(sports_button.text_input)
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    sports_button.used = not sports_button.used
                    sports_button.change_image(used_surface if sports_button.used else button_surface)
                    sports_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif vehicles_button.check_for_input(MOUSE_POS):
                    if (vehicles_button.used):
                        categories.remove(vehicles_button.text_input)
                    else:
                        categories.append(vehicles_button.text_input)
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    vehicles_button.used = not vehicles_button.used
                    vehicles_button.change_image(used_surface if vehicles_button.used else button_surface)
                    vehicles_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                elif music_button.check_for_input(MOUSE_POS):
                    if (music_button.used):
                        categories.remove(music_button.text_input)
                    else:
                        categories.append(music_button.text_input)
                    used_surface = pygame.image.load("assets/used_button.png")
                    used_surface = pygame.transform.scale(used_surface, (450, 100))
                    music_button.used = not music_button.used
                    music_button.change_image(used_surface if music_button.used else button_surface)
                    music_button.update(SCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                
        # Update buttons
        play_button.update(SCREEN)
        play_button.change_color(pygame.mouse.get_pos())
        back_button.update(SCREEN)
        back_button.change_color(pygame.mouse.get_pos())
        easy_button.update(SCREEN)
        easy_button.change_color(pygame.mouse.get_pos())
        normal_button.update(SCREEN)
        normal_button.change_color(pygame.mouse.get_pos())
        hard_button.update(SCREEN)
        hard_button.change_color(pygame.mouse.get_pos())
        history_button.update(SCREEN)
        history_button.change_color(pygame.mouse.get_pos())
        geography_button.update(SCREEN)
        geography_button.change_color(pygame.mouse.get_pos())
        computer_science_button.update(SCREEN)
        computer_science_button.change_color(pygame.mouse.get_pos())
        sports_button.update(SCREEN)
        sports_button.change_color(pygame.mouse.get_pos())
        vehicles_button.update(SCREEN)
        vehicles_button.change_color(pygame.mouse.get_pos())
        music_button.update(SCREEN)
        music_button.change_color(pygame.mouse.get_pos())
        pygame.display.flip()

def lose_screen(mode):
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(background, (1920, 1080))
    lose = pygame.image.load("assets/lost.png")
    lose = pygame.transform.scale(lose, (1200, 500))
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(lose, (390, 180))
    pygame.display.flip()
    button_surface = pygame.image.load("assets/exit_button.webp")
    button_surface = pygame.transform.scale(button_surface, (530, 150))
    retry_button = button.Button(button_surface, 960, 710, "Try again", pygame.font.Font(None, 50))
    back_button = button.Button(button_surface, 960, 810, "Back to main menu", pygame.font.Font(None, 50))
    if mode == "classic":
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
                elif retry_button.check_for_input(pygame.mouse.get_pos()) and mode == "classic":
                    pygame.event.clear()
                    return loading_screen("classic")

def main_menu():
    pygame.mixer.music.load("audio/main_menu_song.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    
    button_surface = pygame.image.load("assets/button.png")
    button_surface = pygame.transform.scale(button_surface, (530, 100))

    play_button = button.Button(button_surface, 960, 550, "PLAY CLASSIC", pygame.font.Font(None, 50))
    endless_button = button.Button(button_surface, 960, 670, "ENDLESS MODE", pygame.font.Font(None, 50))
    exit_button = button.Button(button_surface, 960, 790, "EXIT", pygame.font.Font(None, 50))

    background = pygame.image.load("assets/main_menu_bg.webp")
    background = pygame.transform.scale(background, (1920, 1080))

    title = pygame.image.load("assets/title.png")
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
                    pygame.mixer.music.stop()
                    return loading_screen("classic")
                elif exit_button.check_for_input(MOUSE_POS):
                    pygame.event.clear()
                    pygame.quit()
                elif endless_button.check_for_input(MOUSE_POS):
                    pygame.event.clear()
                    return choose_game_mode_screen()
    
        play_button.update(SCREEN)
        play_button.change_color(pygame.mouse.get_pos())
        exit_button.update(SCREEN)
        exit_button.change_color(pygame.mouse.get_pos())
        endless_button.update(SCREEN)
        endless_button.change_color(pygame.mouse.get_pos())
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
