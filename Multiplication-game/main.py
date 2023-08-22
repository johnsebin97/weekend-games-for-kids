from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

questions = []
total_correct = 0
total_wrong = 0
total_responses = 0
total_time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global questions, total_correct, total_wrong, total_responses, total_time
    questions = generate_questions(10)
    total_correct = 0
    total_wrong = 0
    total_responses = 0
    total_time = 0
    return jsonify({'message': 'Game started!'})

@app.route('/get_question', methods=['GET'])
def get_question():
    if questions:
        question = questions.pop(0)
        return jsonify({'question': question})
    else:
        return jsonify({'question': None})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    global total_correct, total_wrong, total_responses, total_time
    user_answer = int(request.json['answer'])
    elapsed_time = float(request.json['time'])
    correct_answer = request.json['correct_answer']
    
    total_responses += 1
    total_time += elapsed_time
    
    if user_answer == correct_answer:
        total_correct += 1
        return jsonify({'message': 'CORRECT!!', 'response': 'correct'})
    else:
        total_wrong += 1
        return jsonify({'message': 'WRONG ANSWER!', 'response': 'wrong'})

@app.route('/get_results', methods=['GET'])
def get_results():
    if total_responses > 0:
        average_time = total_time / total_correct
        return jsonify({
            'total_correct': total_correct,
            'total_wrong': total_wrong,
            'average_time': average_time,
            'total_time': total_time
        })
    else:
        return jsonify({'message': 'No results yet.'})

def generate_questions(num_questions):
    return [(random.randint(1, 9), random.randint(1, 9)) for _ in range(num_questions)]

if __name__ == '__main__':
    app.run(debug=True)
