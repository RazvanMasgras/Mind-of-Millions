import requests
import html
import random


class NoResponseException(Exception):
    def __init__(self, message="No response received from the Open Trivia Database"):
        self.message = message
        super().__init__(self.message)


cache = []


CATEGORIES = {
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Japanese Anime & Manga": 31,
    "Entertainment: Cartoon & Animations": 32
}


def fetch_trivia_questions(questions=10, category=None, difficulty=None):
    """
    Fetch trivia questions from the Open Trivia Database API.
    Args:
        questions (int, optional): The number of trivia questions to fetch. Defaults to 10.
        category (str, optional): The category of trivia questions. Defaults to None.
        difficulty (str, optional): The difficulty level of trivia questions. Can be 'easy', 'medium', or 'hard'. Defaults to None.
    Returns:
        list: A list of dictionaries, each containing a trivia question and its answers.
    Raises:
        NoResponseException: If the API request fails or returns a non-200 status code.
    """
    url = f"https://opentdb.com/api.php?amount={questions}"

    if category:
        url += f"&category={CATEGORIES.get(category)}"

    if difficulty:
        url += f"&difficulty={difficulty}"

    url += f"&type={'multiple'}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        questions = data.get('results', [])
        for q in questions:
            q['question'] = html.unescape(q['question'])
            q['correct_answer'] = html.unescape(q['correct_answer'])
            q['incorrect_answers'] = [html.unescape(a) for a in q['incorrect_answers']]
        return questions

    raise NoResponseException()


def prepare_questions(questions):
    """
    Prepares a list of trivia questions by shuffling the answers and 
    removing unnecessary fields.
    Args:
        questions (list): A list of dictionaries, where each dictionary 
                          represents a trivia question with the following keys:
                          - 'question' (str): The trivia question.
                          - 'incorrect_answers' (list): A list of incorrect answers.
                          - 'correct_answer' (str): The correct answer.
                          - 'category' (str): The category of the question.
                          - 'type' (str): The type of the question (e.g., multiple choice).
    Returns:
        list: A list of dictionaries, where each dictionary represents a 
              trivia question with the following keys:
              - 'question' (str): The trivia question.
              - 'answers' (list): A shuffled list of answers (including both 
                                  correct and incorrect answers).
              - 'difficulty' (str): The difficulty level of the question.
              - 'correct_answer' (str): The correct answer.
    """
    for q in questions:
        answers = q['incorrect_answers'] + [q['correct_answer']]
        random.shuffle(answers)
        q['answers'] = answers

        # keep only the question, answers, difficulty and correct answer
        q.pop('incorrect_answers')
        q.pop('category')
        q.pop('type')

    return questions


def cache_questions(categories=None, difficulty=None):
    """
    Fetches and caches trivia questions from an external source.
    This function retrieves trivia questions based on the specified categories and difficulty level.
    If no categories are provided, it fetches questions without category restrictions.
    The fetched questions are then prepared and added to the cache.
    Args:
        categories (list, optional): A list of category IDs to fetch questions from. Defaults to None.
        difficulty (str, optional): The difficulty level of the questions ('easy', 'medium', 'hard'). Defaults to None.
    Raises:
        NoResponseException: If the external source does not respond, the function will retry until a response is received.
    Returns:
        None
    """
    questions = []

    if categories is None:
        while True:
            try:
                questions.extend(fetch_trivia_questions(questions=50, difficulty=difficulty))
                break
            except NoResponseException:
                continue
    else:
        for category in categories:
            while True:
                try:
                    questions.extend(fetch_trivia_questions(questions=50, category=category, difficulty=difficulty))
                    break
                except NoResponseException:
                    continue

    questions = prepare_questions(questions)
    cache.extend(questions)


def get_questions_from_cache(difficulty, count):
    """
    Retrieve a specified number of questions from the cache based on difficulty.
    This function filters questions from the cache by the given difficulty level.
    If there are not enough questions in the cache, it will call `cache_questions`
    to fetch more questions until the required count is met. The selected questions
    are then removed from the cache and returned.
    Args:
        difficulty (str): The difficulty level of the questions to retrieve.
        count (int): The number of questions to retrieve.
    Returns:
        list: A list of questions matching the specified difficulty level.
    """
    filtered_questions = [q for q in cache if q['difficulty'] == difficulty]

    while len(filtered_questions) < count:
        cache_questions(difficulty=difficulty)
        filtered_questions = [q for q in cache if q['difficulty'] == difficulty]

    selected_questions = filtered_questions[:count]
    for q in selected_questions:
        cache.remove(q)

    return selected_questions


def gen_normal_mode():
    """
    Generates a list of trivia questions for normal mode.
    This function retrieves a total of 15 questions from the cache, 
    with 5 questions each from the "easy", "medium", and "hard" difficulty levels.
    Returns:
        list: A list of trivia questions.
    """
    questions = []

    questions.extend(get_questions_from_cache("easy", 5))
    questions.extend(get_questions_from_cache("medium", 5))
    questions.extend(get_questions_from_cache("hard", 5))

    return questions


def gen_endless_mode(categories=None, difficulty=None):
    """
    Generate an endless mode of trivia questions.
    This function fetches trivia questions either from all categories or from specified categories,
    shuffles them, and prepares them for use in an endless mode game.
    Parameters:
    categories (list, optional): A list of category IDs to fetch questions from. If None, questions
                                 will be fetched from all categories. Defaults to None.
    difficulty (str, optional): The difficulty level of the questions. Can be 'easy', 'medium', or 'hard'.
                                If None, questions of all difficulties will be fetched. Defaults to None.
    Returns:
    list: A list of prepared trivia questions ready for use in an endless mode game.
    """
    questions = []

    if categories is None:
        questions.extend(fetch_trivia_questions(questions=50, difficulty=difficulty))
    else:
        for category in categories:
            while True:
                try:
                    questions.extend(fetch_trivia_questions(questions=10, category=category, difficulty=difficulty))
                    break
                except NoResponseException:
                    continue

    random.shuffle(questions)

    return prepare_questions(questions)


def correct_answer(question, answer) -> bool:
    """
    Checks if the provided answer is correct for the given question.

    Args:
        question (dict): A dictionary containing the question details, including the 'correct_answer' key.
        answer (str): The answer to be checked.

    Returns:
        bool: True if the answer is correct, False otherwise.
    """
    return question['correct_answer'] == answer


def fifty_fifty(question):
    """
    Modifies the given question dictionary to simulate a "50:50" lifeline by removing two incorrect answers.
    Args:
        question (dict): A dictionary containing the question and its possible answers. 
                         It should have the keys 'answers' (a list of answer options) 
                         and 'correct_answer' (the correct answer string).
    Returns:
        dict: The modified question dictionary with two incorrect answers removed.
    """
    answers = question['answers']
    correct_answer = question['correct_answer']
    incorrect_answer = random.choice([a for a in answers if a != correct_answer])

    for i in range(len(answers)):
        if answers[i] != correct_answer and answers[i] != incorrect_answer:
            answers[i] = ""

    return question


def phone_a_friend(question):
    """
    Simulates the 'Phone a Friend' lifeline by returning the correct answer to the given trivia question.

    Args:
        question (dict): A dictionary containing the trivia question details, including the correct answer.

    Returns:
        str: The correct answer to the trivia question.
    """
    return question["correct_answer"]


def audience_poll(question):
    """
    Simulates an audience poll for a given trivia question and returns the 
    distribution of answers as percentages.
    Args:
        question (dict): A dictionary containing the trivia question details.
            - 'difficulty' (str): The difficulty level of the question ('easy', 'medium', 'hard').
            - 'correct_answer' (str): The correct answer to the question.
            - 'answers' (list): A list of possible answers to the question.
    Returns:
        dict: A dictionary where keys are the possible answers and values are 
        the percentage of the audience that chose each answer.
    """
    weights = {}
    percentage = 100

    if question['difficulty'] == 'easy':
        weights[question['correct_answer']] = random.randint(90, 100)
    elif question['difficulty'] == 'medium':
        weights[question['correct_answer']] = random.randint(70, 90)
    elif question['difficulty'] == 'hard':
        weights[question['correct_answer']] = random.randint(40, 70)

    percentage -= weights[question['correct_answer']]

    for answer in question['answers']:
        if answer != question['correct_answer']:
            if len(weights) < 3:
                weights[answer] = random.randint(0, percentage)
                percentage -= weights[answer]
            else:
                weights[answer] = percentage

    return weights


def change_question(questions, question):
    """
    Replace a specific trivia question with a new one fetched from the trivia API.
    Args:
        questions (list): A list of trivia questions.
        question (dict): The specific trivia question to be replaced. It should contain at least a "difficulty" key.
    Returns:
        list: The updated list of trivia questions with the specified question replaced by a new one.
    Raises:
        NoResponseException: If the trivia API does not respond, the function will keep trying until it succeeds.
    """
    while True:
        try:
            new_question = fetch_trivia_questions(questions=1, difficulty=question["difficulty"])[0]
            break
        except NoResponseException:
            continue

    questions[questions.index(question)] = new_question
    return questions
