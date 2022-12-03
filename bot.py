from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import speech_recognition
import os
from pydub import AudioSegment
from sdk import Dialogflow, Translate, DALLE2

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
        self.dalle = DALLE2()

    @staticmethod
    def add_escape(message):
        special_characters = [".", "-", "_", "+", "(", ")", "!", "[", "]", "&", "*", "="]
        for character in special_characters:
            message = message.replace(character, "\%s" % character, 30)
        return message

    def process(self, text, message):
        if len(text.split(" ")) < 15:
            try:
                intent, response, args, chips = self.dialogflow.get_response(text)
                if intent != "image.imagine":
                    return message.reply_text(self.add_escape(response))
                it_prompt = " ".join(args)
            except Exception as e:
                message.reply_text("Non ho capito cosa mi hai chiesto")
                raise e
        else:
            it_prompt = text

        try:
            en_prompt = self.translate.translate(it_prompt)
        except Exception as e:
            message.reply_text("Non sono riuscito a tradurre la tua richiesta")
            raise e

        try:
            urls = self.dalle.generate_images(en_prompt)
            media = list(map(lambda url: InputMediaPhoto(url), urls))
            media[0].parse_mode = 'MarkdownV2'
            media[0].caption = "*IT prompt*: %s\n*EN prompt*: %s" % (it_prompt, en_prompt)
        except Exception as e:
            message.reply_text("Non sono riuscito a generare la tua immagine, probabilmente hai usato una parola non ammessa")
            raise e

        return message.reply_media_group(media)

    def text_generic(self, update: Update, _: CallbackContext) -> None:
        text = update.message.text
        self.process(text, update.message)

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
        self.process(text, update.message)

    @staticmethod
    def start(update: Update, _: CallbackContext) -> None:
        update.message.reply_text("Benvenuto nel bot di Vox Machina")

    def main_bot(self) -> None:
        self.updater.start_polling()
        self.updater.idle()
