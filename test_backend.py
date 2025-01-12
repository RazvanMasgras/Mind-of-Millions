from open_trivia_db import fifty_fifty, audience_poll, change_question, correct_answer


def test_fifty_fifty():
    question = {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris',
        'incorrect_answers': ['London', 'Berlin', 'Madrid'],
        'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
        'difficulty': 'easy'
    }

    result = fifty_fifty(question)

    assert len(result['answers']) == 4
    assert 'Paris' in result['answers']
    assert result['answers'].count('') == 2
    assert result['answers'].count('Paris') == 1
    assert result['answers'].count('London') + result['answers'].count('Berlin') + result['answers'].count('Madrid') == 1


def test_audience_poll_easy():
    question = {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris',
        'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
        'difficulty': 'easy'
    }

    result = audience_poll(question)

    assert 'Paris' in result
    assert 90 <= result['Paris'] <= 100
    assert sum(result.values()) == 100


def test_audience_poll_medium():
    question = {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris',
        'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
        'difficulty': 'medium'
    }

    result = audience_poll(question)

    assert 'Paris' in result
    assert 70 <= result['Paris'] <= 90
    assert sum(result.values()) == 100


def test_audience_poll_hard():
    question = {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris',
        'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
        'difficulty': 'hard'
    }

    result = audience_poll(question)

    assert 'Paris' in result
    assert 40 <= result['Paris'] <= 70
    assert sum(result.values()) == 100


def test_change_question():
    questions = [
        {
            'question': 'What is the capital of France?',
            'correct_answer': 'Paris',
            'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
            'difficulty': 'easy'
        },
        {
            'question': 'What is the capital of Germany?',
            'correct_answer': 'Berlin',
            'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
            'difficulty': 'easy'
        }
    ]

    original_question = questions[0]
    updated_questions = change_question(questions, original_question)

    assert len(updated_questions) == 2
    assert original_question not in updated_questions
    assert updated_questions[0]['question'] != original_question['question']
    assert updated_questions[0]['difficulty'] == original_question['difficulty']


def test_correct_answer_true():
    question = {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris',
        'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
        'difficulty': 'easy'
    }
    answer = 'Paris'
    assert correct_answer(question, answer) == True


def test_correct_answer_false():
    question = {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris',
        'answers': ['London', 'Berlin', 'Madrid', 'Paris'],
        'difficulty': 'easy'
    }
    answer = 'London'
    assert correct_answer(question, answer) == False
