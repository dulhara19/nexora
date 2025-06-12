from flask import Flask, request, jsonify, render_template
from classifier import classify_and_route
from transformers import MarianMTModel, MarianTokenizer

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Load the multilingual → English translator once at startup
model_name = "Helsinki-NLP/opus-mt-mul-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Translation utilities
def multilingual_to_en(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def detect_and_translate(text: str) -> str:
    # If non-ASCII characters, assume translation needed
    if any(ord(c) > 127 for c in text):
        return multilingual_to_en(text)
    return text  # Already English

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify_endpoint():
    data = request.get_json()
    user_input = data.get("question")

    if not user_input:
        return jsonify({"error": "No question provided."}), 400

    # Translate Sinhala/Tamil to English if needed
    translated_input = detect_and_translate(user_input)

    # Classify with translated text
    result = classify_and_route(translated_input)

    # Include original + translated text in response
    return jsonify({
        "original_input": user_input,
        "translated_input": translated_input,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)
