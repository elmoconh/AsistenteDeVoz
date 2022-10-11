#1 import libreries
import pyaudio
import nltk
nltk.download('omw-1.4')
from neuralintents import GenericAssistant
import speech_recognition 
import pyttsx3 as tts
import sys

#2 define assistant

recognizer = speech_recognition.Recognizer()

""""Gets a reference to an engine instance that will use the given driver. If the requested driver is already in use by another engine instance, that engine is returned. Otherwise, a new engine is created."""
speaker = tts.init()

"""setProperty(name, value) → None
Queues a command to set an engine property. The new property value affects all utterances queued after this command.

Parameters:	
name – Name of the property to change.
value – Value to set.
The following property names are valid for all drivers.

rates
Integer speech rate in words per minute.

voice
String identifier of the active voice.

volume
Floating point volume in the range of 0.0 to 1.0 inclusive."""

speaker.setProperty('rate', 150)

todo_list = ['ir de compras', 'ir al gimnasio']

def create_note():
    global recognizer
    speaker.say('Que nota deseas crear?')
    speaker.runAndWait()

    done = False 

    while not done:
        try:
            with speech_recognition.Microphone() as mic :
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say('Escoje un nombre de archivo')
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = note.lower()

                with open(filename, 'w') as f:
                    f.write(note)
                    done = True
                    speaker.say('Created')
                    speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            speaker.say('Sorry, I did not get that')
            speaker.runAndWait()

def add_to():
    global recognizer
    speaker.say('Quieres agregar algo a tu lista?')
    speaker.runAndWait()
    done = False 

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say('Agregado')   
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            speaker.say('Sorry, I did not get that')
            speaker.runAndWait()

def show_todos():
    speaker.say('Esta es tu lista de tareas')
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say('Hola, bienvenido a tu asistente personal')
    speaker.runAndWait()

def bye():
    speaker.say('Adiós te veo luego')
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "saludo": hello,
    "despedida": bye,
    "crea_nota": create_note,
    "agregar_tarea": add_to,
    "muestra_todo": show_todos
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)

assistant.train_model()

#assistant.request('how are you ??')

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