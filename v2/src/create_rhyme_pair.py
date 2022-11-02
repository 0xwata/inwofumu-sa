# -*- coding: utf-8 -*-

from nltk import tokenize
import random
import csv
import datetime
from wonderwords import RandomWord
import time
import numpy as np
import uuid
from multiprocessing import Pool
from util.tokenizer import Tokenizer, TokenizerSpacy
from util.translate import Translate
from util.ipa_match_word_searcher import IpaMatchWordSearcher
from util.find_syllable_count import find_syllable_count
from util.logging import log_debug, log_error
from util.find_tartget_ipa import find_target_ipa, find_target_ipa_rhyme
from util.format_word_ipa import format_word_ipa

SYLLABLE_MIN_COUNT = 3
N = 100
N_MATCH_MAX = 5

"""
全体の流れ
①ランダムに英単語を選択（品詞は、名詞・形容詞・動詞・副詞）
②言語をランダムに選択して、翻訳（Google Translateの回数制限に注意）
③翻訳した単語をIPA辞書を使って、IPAに変換
④ ③の単語の言語以外の言語でIPA辞書にマッチする単語を検索する
⑤ ③の単語と④のIPAマッチングした単語をCSVに書き込む
"""

"""
   出力テーブル(rhyme_table)を作成する（id必要ないかも)
   | id | word | word_ipa| word_ipa_rhyme | word_lang| word_en | word_ja |  pair_word | pair_word_ipa | pair_word_ipa_rhyme |pair_word_en | pair_word_ja | rhyme_type        | match_ipa_rhyme | pos  | syllable |
   | 19 | hoge | oe      | oe             |   ja     |     ho  | hoge    |  fuga      | ua            |    ua               | hoge        |   fdf        | to or kyaku       | ou        | noun | 3        |
"""


def main():
    output = [["word", "word_lang", "word_ipa",
               "word_ipa_rhyme", "word_en", "word_ja",
               "pair_word", "pair_word_lang", "pair_word_ipa",
               "pair_word_ipa_rhyme", "pair_word_en", "pair_word_ja",
               "rhyme_type", "match_ipa_rhyme", "pos", "syllable"
               ]]
    # 翻訳クラスのインスタンス化
    translate = Translate()
    # IPA変換→マッチング処理のインスタンス化
    ipaMatchWordSearcher = IpaMatchWordSearcher()
    # トークナイザーのインスタンス化
    tokenizer = TokenizerSpacy()

    r = RandomWord()

    for i in range(N):
        request_word_pos = ""
        request_word = "Apple"

        """ 以下の場合、再取得する
        ① 固有名詞の時
        ② tokenizerの結果、品詞情報が得られなかった時
        ③ TODO: 名詞だった時（名詞は動詞、形容詞に比べて３倍近い個数存在するので、品詞の偏りが出ないように70%の確率で却下する 参考：http://user.keio.ac.jp/~rhotta/hellog/2012-06-02-1.html
        """
        # isAccept = False
        while request_word[0].isupper() \
                or request_word_pos == "":
            # or (random_word_pos == "noun" and isAccept is True):
            try:
                request_word = r.word(
                    include_parts_of_speech=["nouns", "verbs", "adjectives"],
                    word_max_length=10
                )

                print(request_word)
                if request_word is None:
                    continue
                request_word_pos = tokenizer.fetch_target_pos(
                    word=request_word,
                    word_en=request_word,
                    lang="en"
                )
                # if random_word_pos == "noun":
                #     isAccept = random.choices([True, False], weights=[0.3, 0.7], k=1)
            except Exception:
                pass
        print(log_debug(f"request_word: {request_word}"))

        langs = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro', 'ar', 'is', 'vi', 'sv', 'fr', 'fi']
        # ランダムに並び替えて初期化
        random.shuffle(langs)

        """
        googleのtranslateのapiに回数制限があるので、
        全ての言語ではなく、シャッフルした上で先頭7個の言語にtranslateする（※ 7個は適当な値）
        """
        for j, lang in enumerate(langs[:7]):
            print(log_debug(f"{str(i)} - {str(j)}"))

            request_word_lang = lang

            request_word_translated = translate.translate_by_language(
                word=request_word,
                lang=request_word_lang
            )
            if request_word_translated == "":
                continue

            print(log_debug(f"request_word_translated: {request_word_translated}"))

            # 音節が少なくとも３つ以上の単語を採用するようにする
            request_word_ipa = ipaMatchWordSearcher.convert_to_ipa(lang=request_word_lang, word=request_word_translated)
            request_word_syllable_count = find_syllable_count(format_word_ipa(request_word_ipa))
            if request_word_syllable_count < SYLLABLE_MIN_COUNT:
                log_error(f"under SYLLABLE_MIN_COUNT, word:{request_word_translated}")
                continue
            # print(log_debug(f"request_word_ipa: {request_word_ipa}"))
            # print(log_debug(f"request_word_syllable_count: {request_word_syllable_count}"))

            # create request_word_pos
            request_word_pos = tokenizer.fetch_target_pos(
                word=request_word_translated,
                word_en=request_word,
                lang=request_word_lang
            )
            if request_word_pos == "":
                log_error("not found part of speech")
                continue
            # print(log_debug(f"request_word_pos: {request_word_pos}"))

            """
            IPA変換→マッチング処理
            """
            # IPA変換処理
            request_word_ipa_rhyme = find_target_ipa_rhyme(request_word_ipa)
            print(log_debug(f"request_word_ipa_rhyme: {request_word_ipa_rhyme}"))

            # IPAベースで韻を踏む単語を探す
            response_dict = ipaMatchWordSearcher.search(
                lang=request_word_lang,
                pos=request_word_pos,
                syllable_count=request_word_syllable_count,
                ipa_rhyme=request_word_ipa_rhyme,
                tokenizer=tokenizer,
                translate=translate
            )
            if response_dict is None:
                print(log_error(f"search error"))
                continue
            elif response_dict["pair_word"] == "":
                print(log_error(f"not found ipa matched word "))
                continue

            response_word = response_dict["pair_word"]
            response_word_lang = response_dict["pair_word_lang"]
            response_word_pos = response_dict["pair_word_pos"]
            response_word_ipa = response_dict["pair_word_ipa"]
            response_word_ipa_rhyme = response_dict["pair_word_ipa_rhyme"]
            rhyme_type = response_dict["rhyme_type"]
            match_ipa_rhyme = response_dict["match_ipa_rhyme"]

            # request
            tmp = []

            print(log_debug("start writing tmp list to output"))
            # write request info
            tmp.append(request_word_translated)
            tmp.append(request_word_lang)
            tmp.append(request_word_ipa)
            tmp.append(request_word_ipa_rhyme)
            tmp.append(
                translate.translate_to_english_by_language(
                    word=request_word_translated,
                    lang=request_word_lang
                )
            )
            tmp.append(
                translate.translate_to_japanese_by_language(
                    word=request_word_translated,
                    lang=request_word_lang
                )
            )
            # write response info

            # --  response
            tmp.append(response_word)
            tmp.append(response_word_lang)
            tmp.append(response_word_ipa)
            tmp.append(response_word_ipa_rhyme)
            tmp.append(
                translate.translate_to_english_by_language(
                    word=response_word,
                    lang=response_word_lang
                )
            )
            tmp.append(
                translate.translate_to_japanese_by_language(
                    word=response_word,
                    lang=response_word_lang
                )
            )
            # -- その他の情報
            tmp.append(rhyme_type)
            tmp.append(match_ipa_rhyme)
            tmp.append(request_word_pos)
            tmp.append(request_word_syllable_count)

            # 各行の書き込み
            output.append(tmp)
            print(log_debug("======================================================================="))
            print(log_debug(f"{tmp}"))
            print(log_debug(f"request_word_pos: {request_word_pos}, response_word_pos: {response_word_pos}"))
            print(log_debug("======================================================================="))

    print(log_debug("start writing output to csv"))
    filename = uuid.uuid1()
    f = open(f'../output/rhyme_pair/v2/{filename}.csv', 'w')
    write = csv.writer(f)
    write.writerows(output)
    print(log_debug(f"finish writing output to csv, length: {len(output)}"))
    print(log_debug(f'filename: {filename}'))


if __name__ == "__main__":
    start = time.time()
    main()
    with Pool(processes=4) as pool:
        pool.map(main(), ())
    elapsed_time = time.time() - start
    print(log_debug("elapsed_time:{0}".format(elapsed_time) + "[sec]"))
