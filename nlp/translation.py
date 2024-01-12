from transformers import pipeline

class EnFrTranslator:
    def __init__(self):
        self.translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

    def translate(self, text):
        translated = self.translator(text)
        return translated[0]['translation_text']

if __name__ == "__main__":
    translator = EnFrTranslator()
    text = "Le temps est beau aujourd'hui"
    translated_text = translator.translate(text)
    print(f"Translated text: {translated_text}")
