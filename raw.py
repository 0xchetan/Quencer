
import sys
import time
import json
import speech_recognition as sr
from gtts import gTTS
import webbrowser
import wikipedia
import os


# obtain audio from the microphone
def listen():
    """
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
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
    """
    user_says = input("Input: ")
    return user_says

#integrating api.ai
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


def main():
    CLIENT_ACCESS_TOKEN = '0dce5f35d7f146a2988c0f69bb702191'
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = "<SESSION ID, PUT YOUR OWN ID HERE>"  
    request.query = listen()
    response = request.getresponse()
    json_file = response.read()
    output=json.loads(json_file)

    response= output["result"]["fulfillment"]["messages"][0]["speech"] 

    print(response)

    get_action_name = output["result"]["action"]



    if get_action_name == "open-app":
        parameter_value = output["result"]["parameters"]["app-name"]
        url = "http://www.google.com/search?q="+parameter_value + "&btnI"
        return webbrowser.open(url)


    if get_action_name == "wiki-search":
        parameter_value = output["result"]["parameters"]["name"]
        wiki_info = wikipedia.summary(parameter_value, sentences=1)
        print(wiki_info)





if __name__ == '__main__':
    

    while True:
        main()

        """
        try:
            main()
        except KeyError:
            print("I am afraid, I can't answer it")
       
"""
