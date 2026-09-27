import time
import webbrowser

import pyttsx3
import speech_recognition as sp


WAKE_WORD = "jarvis"
WAKE_TIMEOUT = 4
WAKE_PHRASE_LIMIT = 3
COMMAND_TIMEOUT = 6
COMMAND_PHRASE_LIMIT = 5
LOOP_DELAY_SECONDS = 0.3


recognizer = sp.Recognizer()
recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.5
engine = pyttsx3.init()


def speak(text):
    engine.stop()
    engine.say(text)
    engine.runAndWait()


def listen_for_text(source, prompt, timeout, phrase_time_limit):
    print(prompt)
    audio = recognizer.listen(
        source,
        timeout=timeout,
        phrase_time_limit=phrase_time_limit,
    )
    text = recognizer.recognize_google(audio).lower().strip()
    print(f"Heard: {text}")
    return text


def handle_command(command):
    words = command.split()
    if not words:
        return

    if words[0] == "open" and len(words) > 1:
        site = words[1].replace(" ", "")
        url = f"https://www.{site}.com"
        webbrowser.open_new_tab(url)
        speak(f"Opening {site}")
        return

    speak("I did not understand the command.")


def run_assistant():
    with sp.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Assistant is ready.")

        while True:
            try:
                wake_text = listen_for_text(
                    source,
                    prompt="Listening for wake word...",
                    timeout=WAKE_TIMEOUT,
                    phrase_time_limit=WAKE_PHRASE_LIMIT,
                )

                if wake_text != WAKE_WORD:
                    time.sleep(LOOP_DELAY_SECONDS)
                    continue

                speak("Yes boss")
                command_text = listen_for_text(
                    source,
                    prompt="Listening for command...",
                    timeout=COMMAND_TIMEOUT,
                    phrase_time_limit=COMMAND_PHRASE_LIMIT,
                )
                handle_command(command_text)

            except sp.WaitTimeoutError:
                print("No speech detected in time.")
            except sp.UnknownValueError:
                print("Could not understand the audio.")
            except sp.RequestError as error:
                print(f"Speech service error: {error}")
                speak("I cannot reach the speech service right now.")
                time.sleep(1)

            time.sleep(LOOP_DELAY_SECONDS)


if __name__ == "__main__":
    run_assistant()





#############################