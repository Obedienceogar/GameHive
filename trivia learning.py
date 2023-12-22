import requests
from urllib.parse import unquote

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://opentdb.com/api.php'

def get_trivia_questions(amount):
    params = {
        'amount': amount,  # Change the number of questions as needed
        'type': 'multiple',  # Multiple-choice questions
        'encode': 'url3986',
        'apiKey': API_KEY,
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        # when i start exception handling in my bot i will modify this part of the code but for now is a pass
        pass

if __name__ == '__main__':
    trivia_questions = get_trivia_questions()
    print(trivia_questions)
    with open('question example.txt','w') as f:
        f.write(str(trivia_questions))
    count = 1
    result = {}
    for i, question_data in enumerate(trivia_questions, start=1):
        question = unquote(question_data['question'])  # Decode the question
        correct_answer = unquote(question_data['correct_answer'])
        incorrect_answers = [unquote(ans) for ans in question_data['incorrect_answers']]  # Decode incorrect answers
        result[str(i)] = {'question':{question},'correct_answer':{correct_answer},'incorrect_answer':{incorrect_answers}}
        print(f'Question {i}: {question}')
        print(f'Correct Answer: {correct_answer}')
        print(f'Incorrect Answers: {", ".join(incorrect_answers)}')
        print('\n')
