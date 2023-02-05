from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import speech_recognition
import os
from pydub import AudioSegment
from sdk import Dialogflow, Translate, OpenAI


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
        self.openai = OpenAI()

    @staticmethod
    def add_escape(message):
        special_characters = [".", "-", "_", "+", "(", ")", "!", "[", "]", "&", "*", "="]
        for character in special_characters:
            message = message.replace(character, "\%s" % character, 30)
        return message

    def process(self, text, update):
        if len(text.split(" ")) < 15:
            try:
                intent, response, args, chips = self.dialogflow.get_response(text)
                if intent != "image.imagine":
                    return self.add_escape(response)
                it_prompt = " ".join(args)
            except Exception as e:
                print(e)
                return update.message.reply_text("Non ho capito cosa mi hai chiesto")
        else:
            it_prompt = text

        try:
            en_prompt = self.translate.translate(it_prompt)
        except Exception as e:
            print(e)
            return update.message.reply_text("Non sono riuscito a tradurre la tua richiesta")

        try:
            urls = self.openai.generate_images(en_prompt)
            media = list(map(lambda url: InputMediaPhoto(url), urls))
        except Exception as e:
            print(e)
            return update.message.reply_text("Non sono riuscito a generare al tua immagine, probabilmente hai usato una parola non ammessa")

        try:
            description = self.openai.generate_description(it_prompt)
        except Exception as e:
            print(e)
            return update.message.reply_text("Errore nella generaione della descrizione")

        try:
            media[0].parse_mode = 'MarkdownV2'
            message = "*Text*: %s\n" % self.add_escape(text)
            message += "*IT prompt*: %s\n" % self.add_escape(it_prompt)
            message += "*EN prompt*: %s\n" % self.add_escape(en_prompt)
            message += "*Description*: %s" % self.add_escape(description)
            media[0].caption = message
            return update.message.reply_media_group(media)
        except Exception as e:
            print(e)
            return update.message.reply_text("Errore nella formattazione del messaggio")

    def text_generic(self, update: Update, _: CallbackContext) -> None:
        text = update.message.text
        return self.process(text, update)

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
            text = ""
        os.remove("audio/file_%s.wav" % chat_id)
        return self.process(text, update)

    @staticmethod
    def start(update: Update, _: CallbackContext) -> None:
        update.message.reply_text("Benvenuto nel bot di Vox Machina")

    def main_bot(self) -> None:
        self.updater.start_polling()
        self.updater.idle()
