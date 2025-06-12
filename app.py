from flask import Flask, request,jsonify,render_template
from classifier import classify_and_route

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify_endpoint():
    data = request.get_json()
    user_input = data.get("question")

    if not user_input:
        return jsonify({"error": "No question provided."}), 400

    result = classify_and_route(user_input)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

