import speech_recognition as sr

def speech_to_text(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("📝 You said:", text)
        return text
    except sr.UnknownValueError:
        print("😕 Sorry, I couldn't understand.")
    except sr.RequestError:
        print("🚫 Service is down or unreachable.")
