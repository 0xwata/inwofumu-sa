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

# 識別対象の母音
VOWELS = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ", "æ"
                "ɐ", "a", "ɶ", "ɑ", "ɒ", "ɚ", "ɑ˞", "ɔ˞"]

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
    "ɔ˞.": "ɔ",
    "a": "ɶ",
    "ɒ": "ɑ",
    "ɑ˞": "ɑ",
    "ɚ": "ə",
}

CONSONANT_PLOSIVE_UNVOICED = ["p", "t", "č", "č", "k", "q"] # -> p
CONSONANT_PLOSIVE_VOICED = ["b", "d", "ǰ", "ɟ", "g", "ɡ", "G", "ʔ"] # -> b
CONSONANT_IMPLOSIVE = ["ɓ", "ɗ", "ɠ"] # -> ɓ
CONSONANT_FRICATIVE_UNVOICED = ["ϕ", "f", "θ", "s", "š", "ɕ", "x", "χ", "ħ"] # -> ϕ
CONSONANT_FRICATIVE_VOICED = ["β", "v", "ð", "z", "ž", "ʑ", "γ", "ʁ", "ʕ"] # -> β
CONSONANT_NASAL = ["m", "ɱ", "n", "ň", "ɲ", "ŋ", "N"] # -> m
CONSONANT_LATERAL_APPPROACH_SOUND = ["l", "Ǐ", "ʎ"] # -> l
CONSONANT_CENTER_APPROXIMATION_SOUND =  ["r", "w", "h"] # -> r

CONSONENTS = CONSONANT_PLOSIVE_UNVOICED + CONSONANT_PLOSIVE_VOICED + \
             CONSONANT_IMPLOSIVE + CONSONANT_FRICATIVE_UNVOICED + CONSONANT_FRICATIVE_VOICED + \
             CONSONANT_NASAL + CONSONANT_LATERAL_APPPROACH_SOUND + CONSONANT_CENTER_APPROXIMATION_SOUND

VOWELS_CONSONENTS = VOWELS + CONSONENTS
VOWELS_CONSONENTS_STRING = ''.join(VOWELS_CONSONENTS)

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
        ipa_vowel_consonents_for_rhyme = convert_to_target_vowels_consonents_for_rhyme(ipa=request_ipa)
        if len(ipa_vowel_consonents_for_rhyme) < N_MATCH:
            return {"word_vowel_matched": "", "lang_vowel_matched": "", "word_vowel_matched_pos": ""}

        # 母音で合致する単語を返す
        response_dict = self.search(lang=lang, ipa_vowel_consonents_for_rhyme=ipa_vowel_consonents_for_rhyme)
        return response_dict


    def search(self, lang: str, ipa_vowel_consonents_for_rhyme: str) -> dict:
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

                ipa_vowel_consonents_for_rhyme_in_line = convert_to_target_vowels_consonents_for_rhyme(ipa_in_line)

                # 末尾 N_MATCH(=3)文字が一致するかどうかをチェック
                if len(ipa_vowel_consonents_for_rhyme) < N_MATCH or len(ipa_vowel_consonents_for_rhyme_in_line) < N_MATCH:
                    continue

                # 整形済みのipa_vowelとipa_vowel_in_lineが一致 && シラブルが一致
                if (new_format_for_is_ipa_rhyme(ipa_vowel_consonents_for_rhyme)[-N_MATCH:] == new_format_for_is_ipa_rhyme(ipa_vowel_consonents_for_rhyme_in_line)[-N_MATCH:]
                    and len(ipa_vowel_consonents_for_rhyme) == len(ipa_vowel_consonents_for_rhyme_in_line) ):
                    print(ipa_vowel_consonents_for_rhyme[-N_MATCH:], ipa_vowel_consonents_for_rhyme_in_line[-N_MATCH:])
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

def convert_to_target_vowels_consonents_for_rhyme(ipa:str ) -> str:
    """[summary]
    Args:
        ipa (str): 例：/ˌkɔɹəˈspɑndənt/（corespondentのIPA)。複数のIPAは返って来ない仕様（今のところ）

    Returns:
        str: 入力したipaの母音を抽出し、連結し、文字列で返却 例：'ɔəɑə'
    """
    return ''.join(re.findall('[' + VOWELS_CONSONENTS_STRING + ']+', ipa))

def new_format_for_is_ipa_rhyme(ipa_word: str) -> str:
    ipa_formatted = ""
    for index, char in enumerate(ipa_word):
        if char in VOWELS:
            if char in SIMILAR_VOWEL_DICT.keys(): #similar_vowel_groupは辞書型
                ipa_formatted  += SIMILAR_VOWEL_DICT[char]
                continue
            ipa_formatted += char
            continue
        ## 以下、子音記号の抽出
        if char in CONSONENTS:
            try:
                next_char = ipa_word[index+1]
                if next_char not in VOWELS:
                    ipa_formatted += map_consonents(char)
            #indexが最後の時も追加する
            except IndexError:
                ipa_formatted += map_consonents(char)
    return ipa_formatted

def map_consonents(char):
    result = ""
    if char in CONSONANT_PLOSIVE_UNVOICED:
        result = "p"
    if char in CONSONANT_PLOSIVE_VOICED:
        result = "b"
    if char in CONSONANT_IMPLOSIVE:
        result = "ɓ"
    if char in CONSONANT_FRICATIVE_UNVOICED:
        result = "ϕ"
    if char in CONSONANT_FRICATIVE_VOICED:
        result = "β"
    if char in CONSONANT_NASAL:
        result = "m"
    if char in CONSONANT_LATERAL_APPPROACH_SOUND:
        result = "l"
    if char in CONSONANT_CENTER_APPROXIMATION_SOUND:
        result = "r"
    return result