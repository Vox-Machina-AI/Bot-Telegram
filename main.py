from bot import Bot
import os
from dotenv import load_dotenv


load_dotenv()


if __name__ == '__main__':
    vox = Bot(os.getenv('TG_TOKEN'))
    vox.main_bot()
