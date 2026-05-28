from flask import Flask, render_template, request, jsonify
import os
import time
import itertools

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# 1. Memory-optimized generator for faster brute-forcing
def your_cracking_function(target_password):
    start_time = time.perf_counter()
    chars = "1234567890"
    length = len(target_password)
    
    # itertools.product generates combinations on-the-fly without consuming RAM
    attempts = 0
    for guess_tuple in itertools.product(chars, repeat=length):
        attempts += 1
        if "".join(guess_tuple) == target_password:
            duration = round(time.perf_counter() - start_time, 4)
            return target_password, attempts, duration
            
    return "", attempts, round(time.perf_counter() - start_time, 4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    # 2. Prevent server crashes if the frontend sends bad JSON data
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
        
    user_password = str(data.get('password', '')).strip()
    
    # 3. Input Validation: Block empty passwords or non-numeric characters
    if not user_password:
        return jsonify({"error": "No password provided"}), 400
        
    if not user_password.isdigit():
        return jsonify({"error": "Only numeric codes (0-9) are allowed"}), 400
        
    # 4. DoS Protection: Restrict length to prevent server CPU overloads
    if len(user_password) > 6:
        return jsonify({"error": "Password too long! Max 6 digits for testing."}), 400

    guessed, attempts, duration = your_cracking_function(user_password)
    
    return jsonify({
        "guessed_password": guessed,
        "attempts": attempts,
        "time_taken": duration
    })

# 5. Production security headers to prevent clickjacking and vulnerabilities
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False) # Turned off debug for safety
