from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello, CI/CD Pipeline!"}), 200

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify({"result": a + b}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)