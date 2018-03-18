
import os.path
import sys
import time
import json
import speech_recognition as sr
from gtts import gTTS


# obtain audio from the microphone
def listen():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        print('Listening...')
        audio=r.listen(source)
    try:
        print("you said:  " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("closing as you're not responding")
        sys.exit()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return r.recognize_google(audio)
    time.sleep(1)


#Speak 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


#integrating api.ai
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '0dce5f35d7f146a2988c0f69bb702191'


def main():
    
    
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, PUT YOUR OWN ID HERE>"

    
    request.query = listen()
    response = request.getresponse()
    json_file = response.read()
    output=json.loads(json_file)
    response= output["result"]["fulfillment"]["messages"][0]["speech"]

    speak(response)

    print(response)


if __name__ == '__main__':
    while True:
        main()