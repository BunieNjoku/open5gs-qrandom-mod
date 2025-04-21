from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/random', methods=['GET'])
def generate_random_number():
    # Generate 16 bytes (128 bits) of random data
    rand_bytes = os.urandom(16)
    # Convert to a hexadecimal string
    rand_hex = rand_bytes.hex()
    print(f"Generated RAND (hex): {rand_hex}")
    return jsonify({'rand': rand_hex})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
