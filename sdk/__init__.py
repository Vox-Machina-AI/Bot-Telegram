from .dialogflow import Dialogflow
from .translate import Translate

import os
image_ai_system = os.getenv('IMAGE_AI_SYSTEM')
match(image_ai_system):
    case 'dalle': from .dalle import DALLE as ImageAI
    case 'dalle2': from .dalle2 import DALLE2 as ImageAI
    case _: raise Exception("Unknown image ai system: " + str(image_ai_system))
