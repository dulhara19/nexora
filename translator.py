from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-mul-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def multilingual_to_en(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def detect_and_translate(text: str) -> str:
    # Simple heuristic: if JSON-escaped letters → assume non-Latin
    if any(ord(c) > 127 for c in text):
        return multilingual_to_en(text)
    return text  # Already English

# Example 
print(detect_and_translate("ඔයා කොහොමද?"))  # Sinhala
print(detect_and_translate("நீங்கள் எப்படி இருக்கிறீர்கள்?"))  # Tamil
print(detect_and_translate("How are you today?"))  # English
