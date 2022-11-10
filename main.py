import pyaudio
import nltk
nltk.download('omw-1.4')
from neuralintents import GenericAssistant
import speech_recognition 
import pyttsx3 as tts
import sys
import os
import subprocess

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)


def open_postman():
    speaker.say('Abriendo Postman')
    speaker.runAndWait()
    user = os.getlogin()
    subprocess.Popen('C:\\Users\\'+user+'\\AppData\\Local\\Postman\\Postman.exe')

def hello():
    speaker.say('Hola, bienvenido a tu asistente personal')
    speaker.runAndWait()

def bye():
    speaker.say('Adiós te veo luego')
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "despedida": bye,
     "postman": open_postman
}

assistant = GenericAssistant('intents.json', intent_methods=mappings, )

assistant.train_model()


while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

            print(message)
            assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()