from flask import jsonify
from src import app

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'up'}), 200
