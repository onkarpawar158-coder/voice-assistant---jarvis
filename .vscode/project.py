import speech_recognition as sp 
import webbrowser 
import pyttsx3
import time
import pywhatkit as kit
import os
from contacts import contact

r = sp.Recognizer()
r.pause_threshold = 0.8
r.non_speaking_duration = 0.5
engine = pyttsx3.init()


def speak(text):  
    engine.say(text)
    engine.runAndWait()



def functio(word):
    message= ""
    words = word.split(" ")
    if words[0] =="open" :
        url = f"https://www.{words[1]}.com"
        webbrowser.open_new_tab(url)
    if words[0] == "play" :
        song=f"{words[1]}"
        kit.playonyt(song)
    if words[0] == "send" :
        for elements in words :
            if elements == words[0] or elements==words[1]:
                continue
            message += elements + " "
        print(words[1])    
        name=contact[words[1]]
        kit.sendwhatmsg_instantly(name,message)
        speak("done")
    


if __name__ == "__main__":
    with sp.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Assistant is ready.")
        while True : 
            r = sp.Recognizer()
            try :
                with sp.Microphone() as source :
                    print("aiktoy...")
                    audio = r.listen(source,timeout=4,phrase_time_limit=3)
                    command =  r.recognize_google(audio) # convert audio into text
                print(command)
                if command.lower() != "jarvis":
                        time.sleep(0.3)
                        continue
                if (command.lower() == "jarvis") :
                    speak("yes boss")
                    with sp.Microphone() as source :
                        audio2 = r.listen(source,timeout=6,phrase_time_limit=5)
                        task =  r.recognize_google(audio2)
                        print(task)
                        functio(task)
              
            except sp.UnknownValueError:
                print("Neet aiku yet nahi")
                        # tasks={"open youtube":"open youtube","open_file_explorer":"open_file_explorer",}
                        # if task in tasks:
            

