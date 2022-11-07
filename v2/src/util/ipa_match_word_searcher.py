# -*- coding: utf-8 -*-

from util.translate import Translate
from util.tokenizer import Tokenizer, TokenizerSpacy
from util.find_syllable_count import find_syllable_count
from util.logging import log_debug, log_error
from util.find_tartget_ipa import find_target_ipa, find_target_ipa_rhyme
from util.find_rhyme_vowel import check_ipa_rhyme_match
from util.format_word_ipa import format_word_ipa
from model.rhyme_type import RhymeType
import re
import time
import random
from typing import Optional

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
## https://github.com/open-dict-data/ipa-dict を参考
LANGS_FOR_SEARCH = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro', 'ar', 'is', 'vi', 'sv', 'fr', 'fi']
LOG_INFO_DEBUG_CLASS_NAME = "CLASS: IpaMatchWordSearcher "
BASE_URL = "../data/ipa-dict/data/"
SYLLABLE_MIN_COUNT = 3


class IpaMatchWordSearcher:
    def __init__(self):
        self.ipa_ja_li = self.read_ipa_data(lang="ja")  ## アラビア語
        self.ipa_en_li = self.read_ipa_data(lang="en_US")  ## 英語
        self.ipa_de_li = self.read_ipa_data(lang="de")  ## ドイツ語
        self.ipa_id_li = self.read_ipa_data(lang="ma")  ## マレー語
        self.ipa_cn_li = self.read_ipa_data(lang="zh_hans") ## 中国語
        self.ipa_ko_li = self.read_ipa_data(lang="ko") ## 韓国語
        self.ipa_eo_li = self.read_ipa_data(lang="eo") ## エスペラント語
        self.ipa_es_ES_li = self.read_ipa_data(lang="es_ES") ## スペイン語
        self.ipa_jam_li = self.read_ipa_data(lang="jam") ## ジャマイカ語
        self.ipa_ro_li = self.read_ipa_data(lang="ro") ## ルーマニア語
        self.ipa_ar_li = self.read_ipa_data(lang="ar") ## アラビア語
        self.ipa_is_li = self.read_ipa_data(lang="is") ## アイスランド語
        self.ipa_vi_li = self.read_ipa_data(lang="vi_C") ## ベトナム語
        self.ipa_sv_li = self.read_ipa_data(lang="sv") ## スウェーデン語
        self.ipa_fr_li = self.read_ipa_data(lang="fr_FR") ## フランス語
        self.ipa_fi_li = self.read_ipa_data(lang="fi") ## フィンランド語
        self.ipa_fa_li = self.read_ipa_data(lang="fa") ## ペルシャ語
        self.ipa_km_li = self.read_ipa_data(lang="km")  ## クメール語
        self.ipa_nb_li = self.read_ipa_data(lang="nb") ## ブークモール（ノルウェー語）
        self.ipa_or_li = self.read_ipa_data(lang="or") ## オリヤー語
        self.ipa_sw_li = self.read_ipa_data(lang="sw") ## スワヒリ語
        self.ipa_tts_li = self.read_ipa_data(lang="tts") ## イーサーン語（タイ語）

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
            "ro": self.ipa_ro_li,
            "ar": self.ipa_ar_li,
            "is": self.ipa_is_li,
            "vi": self.ipa_vi_li,
            "sv": self.ipa_sv_li,
            "fr": self.ipa_fr_li,
            "fi": self.ipa_fi_li,
            "fa": self.ipa_fa_li,
            "km": self.ipa_km_li,
            "nb": self.ipa_nb_li,
            "or": self.ipa_or_li,
            "sw": self.ipa_sw_li,
            "tts": self.ipa_tts_li
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

    def convert_to_ipa(self, lang: str, word: str) -> str:
        ipa_li_target_lang = self.lang_to_ipa_li_for_search[lang]
        ipa = ""
        for line in ipa_li_target_lang:
            if line[0] == word:
                # カンマ区切りで複数のIPAが記載されている場合があるので、簡便のため、最初の要素だけ抽出
                ipa = line[1].split(",")[0] if ("," in line[1]) else line[1]
                break
        if ipa != "":
            print(log_debug(LOG_INFO_DEBUG_CLASS_NAME + "ipa convert Successful"))

        # 改行を削除
        ipa = ipa.replace("\n", "")
        return ipa

    def search(
            self,
            lang: str,
            pos: str,
            ipa_rhyme: str,
            syllable_count: int,
            tokenizer: TokenizerSpacy,
            translate: Translate
    ) -> Optional[dict]:

        """[summary]
        Args:
            ipa_rhyme:
            syllable_count:
            word:
            translate:
            tokenizer:
            pos:
            lang (str): [description]

        Returns:
            list: list[0]= lang, list[1]=word
        """

        # 指定した言語以外を探索するように。
        search_lang_li = list(filter(lambda x: x != lang, LANGS_FOR_SEARCH))
        # ランダムに並び替える
        random.shuffle(search_lang_li)

        flg = False
        pair_word = ""
        pair_word_lang = ""
        pair_word_ipa = ""
        pair_word_ipa_rhyme = ""
        pair_word_pos = ""
        rhyme_type = None
        match_ipa_rhyme = ""

        for lang in search_lang_li:
            print(log_debug("{0} 探索言語：{1}".format(LOG_INFO_DEBUG_CLASS_NAME, lang)))
            pair_word_lang = lang
            ipa_li = self.lang_to_ipa_li_for_search[pair_word_lang]
            random.shuffle(ipa_li)
            count = 0
            for line in ipa_li:
                count += 1
                if count % 10000 == 0:
                    print(count)
                # line[0]:単語 line[1]:IPA
                pair_word = line[0]

                # カンマ区切りで複数のIPAが記載されている場合があるので、簡便のため、最初の要素だけ抽出
                # ipa-dictの**.txtからIPAの部分だけ抽出する処理
                ipa_in_line = line[1].split(",")[0] if ("," in line[1]) else line[1]
                # 改行を削除
                pair_word_ipa = ipa_in_line.replace("\n", "")
                # print(log_debug(f"{LOG_INFO_DEBUG_CLASS_NAME} pair_word_ipa: {pair_word_ipa}"))

                # 音節が少なくとも３つ以上の単語で、音節が3個以上ある単語を採用するようにする
                pair_word_syllable_count = find_syllable_count(format_word_ipa(pair_word_ipa))
                if pair_word_syllable_count < SYLLABLE_MIN_COUNT:
                    log_error("under SYLLABLE_MIN_COUNT")
                    continue
                elif syllable_count != pair_word_syllable_count:
                    log_error("not match syllable count")
                    continue
                # print(log_debug(f"{LOG_INFO_DEBUG_CLASS_NAME} pair_word_ipa: {pair_word_ipa}"))

                pair_word_ipa_rhyme = find_target_ipa_rhyme(pair_word_ipa)

                # 脚韻 or 頭韻を判定
                # FIXME: 頭韻不足のため、頭韻のみ一時的に収集する
                match_ipa_rhyme = check_ipa_rhyme_match(ipa_rhyme, pair_word_ipa_rhyme, RhymeType.TOIN)
                if match_ipa_rhyme is not None:
                    rhyme_type = RhymeType.TOIN.value
                    pair_word_en = translate.translate_to_english_by_language(
                        word=pair_word,
                        lang=pair_word_lang
                    )
                    if pair_word_en == "":
                        print(log_debug(" not found translated word"))
                        continue
                    # print(log_debug(f"{LOG_INFO_DEBUG_CLASS_NAME} pair_word_en: {pair_word_en}"))

                    pair_word_pos = ""
                    pair_word_pos = tokenizer.fetch_target_pos(
                        word=pair_word,
                        word_en=pair_word_en,
                        lang=pair_word_lang
                    )
                    # 同じ品詞ではない場合、skip
                    if pair_word_pos != pos:
                        log_error("not same pos")
                        continue
                    # print(log_debug(f"{LOG_INFO_DEBUG_CLASS_NAME} pair_word_pos: {pair_word_pos}"))
                    flg = True
                    break
                # else:
                #     match_ipa_rhyme = check_ipa_rhyme_match(ipa_rhyme, pair_word_ipa_rhyme, RhymeType.TOIN)

                #     if match_ipa_rhyme is not None:
                #         rhyme_type = RhymeType.TOIN.value
                #         pair_word_en = translate.translate_to_english_by_language(
                #             word=pair_word,
                #             lang=pair_word_lang
                #         )
                #         if pair_word_en == "":
                #             print(log_debug("not found translated word"))
                #             continue
                #         # print(log_debug(f"{LOG_INFO_DEBUG_CLASS_NAME} pair_word_en: {pair_word_en}"))

                #         pair_word_pos = tokenizer.fetch_target_pos(
                #             word=pair_word,
                #             word_en=pair_word_en,
                #             lang=pair_word_lang
                #         )
                #         # 同じ品詞ではない場合、skip
                #         if pair_word_pos != pos:
                #             log_error(" not same pos")
                #             continue
                #         # print(log_debug(f"{LOG_INFO_DEBUG_CLASS_NAME} pair_word_pos: {pair_word_pos}"))
                #         flg = True
                #         break
                #     else:
                #         log_error(" not match ipa rhyme")
                #         continue
            if flg:
                print(log_debug("Loop stop"))
                break
        print(log_debug("Loop finish"))

        return {
            "pair_word": pair_word,
            "pair_word_lang": pair_word_lang,
            "pair_word_ipa": pair_word_ipa,
            "pair_word_ipa_rhyme": pair_word_ipa_rhyme,
            "pair_word_pos": pair_word_pos,
            "rhyme_type": rhyme_type,
            "match_ipa_rhyme": match_ipa_rhyme,
        }
