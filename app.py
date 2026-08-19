
from flask import Flask, jsonify
from routes import inventory_bp

app = Flask(__name__)
app.register_blueprint(inventory_bp)


@app.route("/")
def index():
    return jsonify({"message": "Inventory API is running"})


if __name__ == "__main__":
    app.run(debug=True)