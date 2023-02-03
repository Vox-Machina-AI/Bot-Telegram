# Vox Machina - Telegram Bot
Chat bot Telegram che disegna immagini. In italiano!

Scrivi a [@VoxMachinaBot](https://t.me/VoxMachinaBot) su Telegram per provare.

Chiedi di disegnare qualcosa e attendi il risultato. Puoi anche mandare un messaggio vocale.

## Setup for developers
### Environment variables
Environment variables are read from the operating system or from a `.env` file.

These variables need to be defined in order for the bot to work properly:
- `TG_TOKEN`: Telegram token acquired from the BotFather.
- `OPENAI_TOKEN`: OpenAI api key.
- `DIALOGFLOW_AGENT`: Dialogflow agent.
- `DIALOGFLOW_CREDENTIAL`: Dialogflow credentials.
- `GOOGLE_APPLICATION_CREDENTIALS`: Google application credentials.

### Service accounts
- Chat to the [BotFather](https://t.me/botfather) on Telegram to register your bot and receive its authentication token.
- If you want to use the OpenAI Image API, navigate to the [Api Keys](https://beta.openai.com/account/api-keys) section to create an api key.
- Setup a new Dialogflow agent. Docs [here](https://cloud.google.com/dialogflow/es/docs/quick/setup).

### Run bot
Python3 with pip is required. We recommend to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to install Python dependencies.

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Run bot:
```bash
python3 main.py
```