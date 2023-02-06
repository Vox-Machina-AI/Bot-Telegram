import openai
import os
import random


class OpenAI:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_TOKEN')
        self.dalle = openai.Image
        self.gpt = openai.Completion

    def generate_images(self, prompt):
        images = self.dalle.create(prompt=prompt, n=1, size="1024x1024")['data']
        return list(map(lambda img: img['url'], images))

    def generate_description(self, prompt):
        prompt_array = [
            "impersona un un critico d'arte famoso e descrivi brevemente una immagine che raffigura %s" % prompt,
            "descrivi brevemente che cosa vedi nell'immagine che ritrae %s" % prompt,
            "quali sono i dettagli più importanti dell'immagine che rappresenta %s" % prompt
        ]

        completion = self.gpt.create(engine="text-davinci-003", 
                                     prompt=random.choices(prompt_array),
                                     max_tokens=150,
                                     temperature=0.7)
        return completion.choices[0].text
