from flask import Flask, render_template, request, jsonify
import os
import time
import random
import itertools

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)


def your_cracking_function(target_password):
    start_time = time.perf_counter()
    chars = "1234567890"
    attempts = 0
    length = len(target_password)
    
    # Generate sequential combinations of the exact length needed
    for guess_tuple in itertools.product(chars, repeat=length):
        attempts += 1
        guess = "".join(guess_tuple)
        
        if guess == target_password:
            end_time = time.perf_counter()
            duration = round(end_time - start_time, 4)
            return guess, attempts, duration
            
    # Fallback return if somehow not found
    end_time = time.perf_counter()
    return "", attempts, round(end_time - start_time, 4)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    data = request.json
    user_password = data.get('password', '')
    
    if not user_password:
        return jsonify({"error": "No password provided"}), 400

    # Run the function and get results
    guessed, attempts, duration = your_cracking_function(str(user_password))
    
    return jsonify({
        "guessed_password": guessed,
        "attempts": attempts,
        "time_taken": duration
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
