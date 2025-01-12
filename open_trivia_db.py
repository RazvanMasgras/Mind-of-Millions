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
    "Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Computer Science": 18,
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
    filtered_questions = [q for q in cache if q['difficulty'] == difficulty]

    while len(filtered_questions) < count:
        cache_questions(difficulty=difficulty)
        filtered_questions = [q for q in cache if q['difficulty'] == difficulty]

    selected_questions = filtered_questions[:count]
    for q in selected_questions:
        cache.remove(q)

    return selected_questions


def gen_normal_mode():
    questions = []

    questions.extend(get_questions_from_cache("easy", 5))
    questions.extend(get_questions_from_cache("medium", 5))
    questions.extend(get_questions_from_cache("hard", 5))

    return questions


def gen_endless_mode(categories=None, difficulty=None):
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
    return question['correct_answer'] == answer


def fifty_fifty(question):
    answers = question['answers']
    correct_answer = question['correct_answer']
    incorrect_answer = random.choice([a for a in answers if a != correct_answer])

    for i in range(len(answers)):
        if answers[i] != correct_answer and answers[i] != incorrect_answer:
            answers[i] = ""

    return question


def phone_a_friend(question):
    return question["correct_answer"]


def audience_poll(question):
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
    while True:
        try:
            new_question = fetch_trivia_questions(questions=1, difficulty=question["difficulty"])[0]
            break
        except NoResponseException:
            continue

    questions[questions.index(question)] = new_question
    return questions
