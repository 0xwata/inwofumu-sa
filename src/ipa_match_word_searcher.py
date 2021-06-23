from translate import Translate
from tokenizer import Tokenizer, TokenizerSpacy
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
    ・エスペラント語
        'eo', Esperanto
    ・スペイン語
        'es_ES', Spanish (Spain),
    ・ジャマイカ語
        'jam', Jamaican Creole
    ・ルーマニア語
        'ro', Romanian
"""

LOG_INFO_DEBUG = "LOG/DEBUG: "
LOG_INFO_DEBUG_CLASS_NAME = "CLASS: IpaMatchWordSearcher "


BASE_URL = "../data/ipa-dict/data/"

# https://www.ipachart.com/
# 上記のvowelを採用する
# 鼻音も追加
# https://ekimeihyo.net/o/ipa.html
VOWELS_LI = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ",
          "æ", "ɐ", "a", "ɶ", "ɑ", "ɒ","m̥","m","ɱ","n̼̊","n̼","n̥","n","ɳ̊","ɳ","ɲ̊","ɲ","ŋ̊","ŋ","ɴ̥","ɴ"]
VOWELS = ''.join(VOWELS_LI)

# 似ているアクセントに変換する辞書
SIMILAR_VOWEL_DICT = {
    "i":"y",
    "ɨ": "ʉ",
    "ɯ": "u",
    "ɪ": "ʏ",
    "e": "ø",
    "ɤ": "o",
    "ɛ": "œ",
    "ɜ": "ɞ",
    "ʌ": "ɔ",
    "a": "ɶ",
    "ɑ": "ɒ"
}

NASAL_DICT = ["m̥","m","ɱ","n̼̊","n̼","n̥","n","ɳ̊","ɳ","ɲ̊","ɲ","ŋ̊","ŋ","ɴ̥","ɴ"]

LANGS_FOR_SEARCH = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro']

N_MATCH = 3

class IpaMatchWordSearcher:
    def __init__(self):
        self.ipa_ja_li = self.read_ipa_data(lang="ja")
        self.ipa_en_li = self.read_ipa_data(lang="en_US")
        self.ipa_de_li = self.read_ipa_data(lang="de")
        self.ipa_id_li = self.read_ipa_data(lang="ma")
        self.ipa_cn_li = self.read_ipa_data(lang="zh_hans")
        self.ipa_ko_li = self.read_ipa_data(lang="ko")
        self.ipa_eo_li = self.read_ipa_data(lang="eo")
        self.ipa_es_ES_li = self.read_ipa_data(lang="es_ES")
        self.ipa_jam_li = self.read_ipa_data(lang="jam")
        self.ipa_ro_li = self.read_ipa_data(lang="ro")
        self.lang_to_ipa_li_for_search = {
            "ja": self.ipa_ja_li,
            "en": self.ipa_en_li,
            "de": self.ipa_de_li,
            "id": self.ipa_id_li,
            "zh-cn": self.ipa_cn_li,
            "ko": self.ipa_ko_li,
            "eo": self.ipa_eo_li,
            "es": self.ipa_es_ES_li,
            "jam": self.ipa_jam_li,
            "ro": self.ipa_ro_li
        }

    def read_ipa_data(self, lang: str) -> list:
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
        return ipa_list

    def execute(self, word: str, lang: str) -> dict:
        """[summary]

        Args:
            words ([str]): [description]
            lang ([str]): [description]
            pos ([str]): part of speech
        """
        request_ipa = self.convert_to_ipa(lang=lang, word=word)
        if request_ipa == "":
            return {"word_vowel_matched": "", "lang_vowel_matched": "", "word_vowel_matched_pos": ""}
        # IPAの中から、母音の部分を抜き出す
        ipa_vowel = self.detect_vowel(ipa=request_ipa)
        if len(ipa_vowel) < N_MATCH:
            return {"word_vowel_matched": "", "lang_vowel_matched": "", "word_vowel_matched_pos": ""}

        # 母音で合致する単語を返す
        response_dict = self.search(lang=lang, ipa_vowel=ipa_vowel)
        return response_dict


    def search(self, lang: str, ipa_vowel: str) -> dict:
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

        flg = False
        word_vowel_matched = ""
        lang_vowel_matched = ""
        word_vowel_matched_pos = ""
        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + f"{search_lang_li}")
        for lang in search_lang_li:
            print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + f"探索言語：{lang}")
            ipa_li = self.lang_to_ipa_li_for_search[lang]
            for line in ipa_li:
                # line[0]:単語 line[1]:IPA

                # カンマ区切りで複数のIPAが記載されている場合があるので、簡便のため、最初の要素だけ抽出
                ipa_in_line = line[1].split(",")[0] if ("," in line[1]) else line[1]
                # 改行を削除
                ipa_in_line = ipa_in_line.replace("\n", "")

                ipa_vowel_in_line = self.convert_to_vowel(ipa_in_line)

                # 末尾 N_MATCH(=3)文字が一致するかどうかをチェック
                if len(ipa_vowel) < N_MATCH or len(ipa_vowel_in_line) < N_MATCH:
                    continue

                # 整形済みのipa_vowelとipa_vowel_in_lineが一致 && シラブルが一致
                if self.format_for_is_ipa_rhyme(ipa_vowel)[-N_MATCH:] == self.format_for_is_ipa_rhyme(ipa_vowel_in_line)[-N_MATCH:] and len(ipa_vowel) == len(ipa_vowel_in_line):
                    print(ipa_vowel[-N_MATCH:], ipa_vowel_in_line[-N_MATCH:])
                    word_vowel_matched = line[0]
                    lang_vowel_matched = lang

                    """
                    マッチング済み単語の翻訳処理
                    """
                    word_en_vowel_matched = Translate().translate_to_english_by_language(word=word_vowel_matched, lang=lang_vowel_matched)

                    """
                    マッチング済み単語の品詞推定処理
                    """
                    if word_en_vowel_matched != "":
                        # word_vowel_matched_pos = Tokenizer().fetch_target_pos(word=word_en_vowel_matched)
                        #spacyによる品詞推定
                        word_vowel_matched_pos = TokenizerSpacy().fetch_target_pos(word=word_vowel_matched, word_en=word_en_vowel_matched, lang=lang_vowel_matched)


                    if word_vowel_matched_pos != "":
                        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "Found the word matched IPA vowel")
                        flg = True
                        break
            if flg:
                print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "Loop stop")
                break
        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "Loop finish")
        print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + f"word_vowel_matched = {word_vowel_matched}, lang_vowel_matched = {lang_vowel_matched}, word_vowe_matched_pos = {word_vowel_matched_pos}")

        return {"word_vowel_matched": word_vowel_matched, "lang_vowel_matched": lang_vowel_matched, "word_vowel_matched_pos": word_vowel_matched_pos}

    def detect_vowel(self, ipa: str) -> str:
        """[summary]
        https://www.ipachart.com/
        ここのvowelを採用する

        Args:
            ipa (str): 例：/ˌkɔɹəˈspɑndənt/（corespondentのIPA)。複数のIPAは返って来ない仕様（今のところ）

        Returns:
            str: 入力したipaの母音を抽出し、連結し、文字列で返却 例：'ɔəɑə'
        """
        return ''.join(re.findall('[' + VOWELS + ']+', ipa))

    def format_for_is_ipa_rhyme(self, vowel_and_nasal:str) -> str:
        """[summary]
        IPAの一致を測るためだけに整形する文字列を作成する

        https://www.ipachart.com/
        VOWELS_LI = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ",
          "æ", "ɐ", "a", "ɶ", "ɑ", "ɒ"]
        """
        formatted_string = ""
        for char in vowel_and_nasal:
            # 類似のIPAは片方に変換する
            if char in SIMILAR_VOWEL_DICT.keys():
                formatted_string += SIMILAR_VOWEL_DICT[char]
                continue

            #　鼻音は全てnに変換
            if char in NASAL_DICT:
                formatted_string += "n"
                continue

            formatted_string += char
        return formatted_string

    def convert_to_vowel(self, ipa:str ) -> str:
        return ''.join(re.findall('[' + VOWELS + ']+', ipa))

    def convert_to_ipa(self, lang: str, word: str) -> str:
        ipa_li_target_lang = self.lang_to_ipa_li_for_search[lang]
        ipa = ""
        for line in ipa_li_target_lang:
            if line[0] == word:
                # カンマ区切りで複数のIPAが記載されている場合があるので、簡便のため、最初の要素だけ抽出
                ipa = line[1].split(",")[0] if ("," in line[1]) else line[1]
                break
        if (ipa != ""):
            print(LOG_INFO_DEBUG + LOG_INFO_DEBUG_CLASS_NAME + "ipa convert Successful")

        # 改行を削除
        ipa = ipa.replace("\n", "")
        return ipa
