# app.py
from flask import Flask, jsonify

app = Flask(__name__)

# Ruta GET para sena Time to Live
@app.route(
    '/ttl', 
    methods=['GET']
)
def ttl():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)