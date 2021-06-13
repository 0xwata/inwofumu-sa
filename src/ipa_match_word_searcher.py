from translate import Translate
from tokenizer import Tokenizer
import re
import time
import random
"""
対象言語：
    ・日本語:
        ja.txt
    ・英語:
        en_US.txt
    ・ドイツ語:
        de.txt
    ・インドネシア語:
        ma.txt Malay (Malaysian and Indonesian)
    ・中国語:
        yue.txt Cantonese
        zh_hans.txt(simplified), zh_hant.txt(traditional) Mandarin
    ・韓国語:
        ko.txt Korean
    ・ロシア語
        https://github.com/open-dict-data/ipa-dict/tree/master/data
        ここにデータがない
"""

LOG_INFO_DEBUG = "LOG/DEBUG: "
LOG_INFO_DEBUG_CLASS_NAME = "CLASS: IpaMatchWordSearcher "

CONVERTER_DIC_FOR_URL = {
    "ja" : "ja",
    "en" : "en",
    "de" : "de",
    "id" : "ma",
    "zh-cn" : "zh"
}

BASE_URL = "../data/ipa-dict/data/"

# https://www.ipachart.com/
# 上記のvowelを採用する
VOWELS = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ", "æ", "ɐ", "a", "ɶ", "ɑ", "ɒ"]

LANGS_FOR_SEARCH = ["ja", "en", "de", "id", "zh-cn", "ko"]

class IpaMatchWordSearcher:
    def __init__(self):
        self.converter_dic_for_url = CONVERTER_DIC_FOR_URL
        self.ipa_ja_li = self.read_ipa_data(lang = "ja")
        self.ipa_en_li = self.read_ipa_data(lang = "en_US")
        self.ipa_de_li = self.read_ipa_data(lang = "de")
        self.ipa_id_li = self.read_ipa_data(lang = "ma")
        self.ipa_cn_li = self.read_ipa_data(lang = "zh_hans")
        self.ipa_ko_li = self.read_ipa_data(lang = "ko")
        self.lang_to_ipa_li_for_search = {
            "ja": self.ipa_ja_li,
            "en": self.ipa_en_li,
            "de": self.ipa_de_li,
            "id": self.ipa_id_li,
            "zh-cn": self.ipa_cn_li,
            "ko": self.ipa_ko_li
        }

    def read_ipa_data(self, lang:str) -> list:
        """[summary]

        Args:
            lang (str): [description]

        Returns:
            list:
                中身：単語 \t IPA
        """
        ipa_list = []
        with open(BASE_URL + lang + ".txt") as file:
            for s_line in file:
                ipa_list.append(s_line.split('\t'))
        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + lang+".textの読み込みを完了")
        return ipa_list

    def execute_v2(self, word: str, lang:str, pos: str):
        """[summary]

        Args:
            words ([str]): [description]
            lang ([str]): [description]
            pos ([str]): part of speech
        """
        if lang == 'ru':
            #ロシア語のIPA
            #そもそもhttps://github.com/open-dict-data/ipa-dictにデータがない言語
            return ["", ""]
        else:
            tmp = self.convert_by_ipa_li(lang = lang, word = word)
            if tmp == "":
                return ["", ""]
            ipa = tmp
        # IPAの中から、母音の部分を抜き出す
        ipa_vowel = self.detect_vowel(ipa = ipa)

        # 母音で合致する単語を探す
        response_lang, response_word = self.search(lang = lang, ipa_vowel = ipa_vowel, pos = pos)
        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + response_lang, response_word)
        return [response_word, response_lang]
    def execute(self, words: dict, pos: str):
        """[summary]

        Args:
            words ([dict]): [description]
            pos ([str]): part of speech
        """

        request_word = ""
        request_lang = ""
        response_word = ""
        response_lang = ""
        for k, v in words.items():
            # 各翻訳された単語についてIPA変換
            if k == 'ru':
                #ロシア語のIPA
                #そもそもhttps://github.com/open-dict-data/ipa-dictにデータがない言語
                continue
            else:
                tmp = self.convert_by_ipa_li(lang = k, word = v)
                if tmp == "":
                    continue
                ipa = tmp

            # IPAの中から、母音の部分を抜き出す
            ipa_vowel = self.detect_vowel(ipa = ipa)

            # 母音で合致する単語を探す
            response_lang, response_word = self.search(lang = k, ipa_vowel = ipa_vowel, pos = pos)
            print(response_lang, type(response_lang))
            print(response_word, type(response_word))
            if response_lang != "" and response_word != "":
                request_lang = k
                request_word = v
                break

        if request_word != "":
            request_dict = {
                "word": request_word,
                "lang": request_lang
            }
        else:
            request_dict = {}

        if response_word != "":
            response_dict = {
                "word": response_word,
                "lang": response_lang
            }
        else:
            response_dict = {}

        return [request_dict, response_dict]

    def search(self, lang:str, ipa_vowel:str, pos:str) -> list:
        """[summary]

        Args:
            lang (str): [description]
            vowel (str): [description]

        Returns:
            list: list[0]= lang, list[1]=word
        """
        # 指定した言語以外を探索するように。
        search_lang_li = list(filter(lambda x: x != lang, LANGS_FOR_SEARCH))
        # ランダムに並び替える
        random.shuffle(search_lang_li)

        joined_vowels = ''.join(VOWELS)
        flg = False
        pos_flg = False
        lang = ""
        word = ""
        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + f"{search_lang_li}")
        for i in search_lang_li:
            print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + f"探索言語：{i}")
            ipa_li = self.lang_to_ipa_li_for_search[i]
            for line in ipa_li:
                #line[0]:単語 line[1]:IPA

                # カンマ区切りで複数のIPAが記載されている場合があるので、簡便のため、最初の要素だけ抽出
                ipa_in_line = line[1].split(",")[0] if ("," in line[1]) else line[1]

                ipa_vowel_in_line = ''.join(re.findall('['+joined_vowels+']+', ipa_in_line))

                if(ipa_vowel == ipa_vowel_in_line):
                    word = line[0]
                    lang = i
                    """
                    マッチング済み単語の翻訳処理
                    """
                    word_en = Translate().translate_to_english_by_language(word=word, lang=lang)

                    """
                    マッチング済み単語の品詞推定処理
                    """
                    if word_en != "":
                        pos_flg = Tokenizer().is_target_pos(word = word_en, target_pos = pos)

                    if pos_flg:
                        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "Found the word matched IPA vowel")
                        flg = True
                        break
            if flg:
                print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "Loop stop")
                break
        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "Loop finish")
        return [lang, word]


    def detect_vowel(self, ipa:str) -> str:
        """[summary]
        https://www.ipachart.com/
        ここのvowelを採用する

        Args:
            ipa (str): 例：/ˌkɔɹəˈspɑndənt/（corespondentのIPA)。複数のIPAは返って来ない仕様（今のところ）

        Returns:
            str: 入力したipaの母音を抽出し、連結し、文字列で返却 例：'ɔəɑə'
        """
        joined_vowels = ''.join(VOWELS)
        return ''.join(re.findall('['+joined_vowels+']+', ipa))

    def convert_by_ipa_li(self, lang: str, word: str) -> str:
        ipa_li_target_lang = self.lang_to_ipa_li_for_search[lang]
        ipa = ""
        for line in ipa_li_target_lang:
            if line[0] == word:
                # カンマ区切りで複数のIPAが記載されている場合があるので、簡便のため、最初の要素だけ抽出
                ipa = line[1].split(",")[0] if ("," in line[1]) else line[1]
                break
        if(ipa != ""):
            print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "ipa convert Successful")
        return ipa

