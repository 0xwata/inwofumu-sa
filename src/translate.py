from googletrans import Translator
import random
"""
対象言語：
    ・日本語:
        'ja': 'japanese',
    ・英語:
        'en': 'english',
    ・ドイツ語:
        'de': 'german',
    ・インドネシア語:
        'id': 'indonesian',
    ・中国語:
        'zh-cn': 'chinese (simplified)',
        'zh-tw': 'chinese (traditional)',
    ・韓国語:
        'ko': 'korean',
    ・ロシア語
        'ru': 'russian'
"""
class Translate:
    def __init__(self):
        self.translator = Translator()
        self.langs = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'ru']

    def translate_all_language(self, word: str) -> dict:
        #ランダムに並び替えて初期化
        langs_random_sort = random.shuffle(self.langs)

        translated_words = {}
        for lang in langs_random_sort:
            translated_words[lang] = self.translator.translate(word, dest=lang)
        return translated_words

    def translate_by_language(self, word: str, lang: str) -> str:
        return self.translator.translate(word, dest=lang)
