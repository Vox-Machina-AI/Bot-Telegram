from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import speech_recognition
import os
from pydub import AudioSegment
from sdk import Dialogflow, Translate, DALLE


class Bot:
    def __init__(self, bot_token):
        self.updater = Updater(bot_token)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text_generic))
        self.dispatcher.add_handler(MessageHandler(Filters.voice, self.audio_generic))

        self.recognizer = speech_recognition.Recognizer()
        self.dialogflow = Dialogflow()
        self.translate = Translate()
        self.dalle = DALLE()

    @staticmethod
    def add_escape(message):
        special_characters = [".", "-", "_", "+", "(", ")", "!", "[", "]", "&", "*", "="]
        for character in special_characters:
            message = message.replace(character, "\%s" % character, 30)
        return message

    def create_img_message(self, text, it_prompt, en_prompt, image_url):
        message = "*Text*: %s\n" % self.add_escape(text)
        message += "*IT prompt*: %s\n" % self.add_escape(it_prompt)
        message += "*EN prompt*: %s\n" % self.add_escape(en_prompt)
        message += "*Image url*: %s" % self.add_escape(image_url)
        return message

    def create_intent_message(self, intent, text):
        message = "*Intent*: %s\n" % self.add_escape(intent)
        message += "*Text*: %s" % self.add_escape(text)
        return message

    def process(self, text):
        intent, response, args, chips = self.dialogflow.get_response(text)
        if args == "":
            return self.create_intent_message(intent, response)
        it_prompt = " ".join(args)
        en_prompt = self.translate.translate(it_prompt)
        image_url = self.dalle.generate_image(en_prompt)
        return self.create_img_message(text, it_prompt, en_prompt, image_url)

    def text_generic(self, update: Update, _: CallbackContext) -> None:
        text = update.message.text
        update.message.reply_text(self.process(text), parse_mode='MarkdownV2')

    def audio_generic(self, update: Update, context: CallbackContext) -> None:
        chat_id = str(update.message.chat_id)
        context.bot.get_file(update.message.voice.file_id).download("audio/file_%s.ogg" % chat_id)
        audio_file = AudioSegment.from_ogg("audio/file_%s.ogg" % chat_id)
        audio_file.export("audio/file_%s.wav" % chat_id, format="wav")

        try:
            with speech_recognition.AudioFile("audio/file_%s.wav" % chat_id) as source:
                audio = self.recognizer.record(source, duration=7)
                text = self.recognizer.recognize_google(audio, language="it-IT")
        except speech_recognition.UnknownValueError:
            text = ""
        except speech_recognition.RequestError:
            text = ""
        except Exception as e:
            print(e)
            text = "error"
        os.remove("audio/file_%s.wav" % chat_id)
        update.message.reply_text(self.process(text), parse_mode='MarkdownV2')

    @staticmethod
    def start(update: Update, _: CallbackContext) -> None:
        update.message.reply_text("Benvenuto nel bot di Vox Machina")

    def main_bot(self) -> None:
        self.updater.start_polling()
        self.updater.idle()