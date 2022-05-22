import pyttsx3


class Audio:
    text = '你好'

    def __init__(self, texts):
        self.text = texts

    def setter(self, texts):
        self.text = texts

    def say(self):
        engine = pyttsx3.init()

        engine.say(self.text)
        engine.runAndWait()
