from googletrans import Translator


class Translate:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text):
        return self.translator.translate(text, src='it', dest='en').text
