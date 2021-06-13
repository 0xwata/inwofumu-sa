from googletrans import Translator
import random
import httpcore
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
        random.shuffle(self.langs)
        translated_words = {}
        print("inputした単語:"+word)
        print("以下、翻訳")
        for lang in self.langs:
            if lang == "en":
                translated_words[lang] = word
                print(lang, word)

            else:
                try:
                    translated_word = self.translator.translate(word, dest=lang).text
                    translated_words[lang] = translated_word
                    print(lang, translated_word)
                except httpcore._exceptions.ReadTimeout as e:
                    print("エラー" , e)
        print("翻訳終了")

        return translated_words

    def translate_by_language(self, word: str, lang:str) -> str:
        translated_word = ""
        try:
            translated_word = self.translator.translate(word, dest=lang, src='en').text
        except httpcore._exceptions.ReadTimeout as e:
            print("エラー" , e)
        return translated_word



    def translate_to_english_by_language(self, word: str, lang: str) -> str:
        translated_word = ""
        try:
            translated_word = self.translator.translate(word, dest='en', src=lang).text
        except httpcore._exceptions.ReadTimeout as e:
            print("エラー" , e)
        return translated_word
