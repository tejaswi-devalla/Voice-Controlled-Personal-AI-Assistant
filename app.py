from transformers import pipeline
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia

# Load free GPT-2 model
chatbot = pipeline('text-generation', model='gpt2')

# Text-to-speech engine setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand(prompt=False):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt:
            print(prompt)
            speak(prompt)
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception:
            print("Could not understand. Please say that again.")
            return "None"
    return query

def Reply(question):
    result = chatbot(question, max_length=100, do_sample=True)[0]['generated_text']
    return result

if __name__ == '__main__':
    speak("Assistant is ready. Say Hey AI or ok AI to activate.")
    while True:
        query = takeCommand().lower()
        if query == "none":
            continue

        if "hey ai" in query or "ok ai" in query:
            speak("Hey! How can I help you?")
            while True:
                query = takeCommand().lower()

                if query == "none":
                    continue

                if "open youtube" in query:
                    speak("Opening YouTube.")
                    webbrowser.open('https://www.youtube.com')
                    continue

                if "open google" in query:
                    speak("Opening Google.")
                    webbrowser.open('https://www.google.com')
                    continue

                if "time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"The time is {strTime}")
                    continue

                if 'who is' in query or 'what is' in query:
                    speak('Searching Wikipedia...')
                    query = query.replace("who is", "").replace("what is", "").strip()
                    try:
                        results = wikipedia.summary(query, sentences=2)
                        speak("According to Wikipedia...")
                        print(results)
                        speak(results)
                    except Exception as e:
                        speak("Sorry, I could not find any results.")
                    continue

                if "bye" in query or "goodbye" in query:
                    speak("Goodbye! See you later.")
                    exit()

                # If no special command, use local chatbot
                ans = Reply(query)
                print(ans)
                speak(ans)
