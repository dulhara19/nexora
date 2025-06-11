import speech_recognition as sr

def speech_to_text():
  # Initialize recognizer
 recognizer = sr.Recognizer()

 with sr.Microphone() as source:
    print("🎙️ Speak something...")
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("📝 You said:", text)
    except sr.UnknownValueError:
        print("😕 Sorry, I couldn't understand.")
    except sr.RequestError:
        print("🚫 Service is down or unreachable.")
