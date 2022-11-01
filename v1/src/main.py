from nltk import tokenize
# from adjective_noun_pair import AdjectiveNounPairSelector
from tokenizer import Tokenizer, TokenizerSpacy
from translate import Translate
from ipa_match_word_searcher import IpaMatchWordSearcher, new_format_for_ipa_rhyme, convert_to_target_vowels_consonants_for_rhyme
from ipa_match_word_searcher_v2 import IpaMatchWordSearcher, new_format_for_ipa_rhyme, convert_to_target_vowels_consonants_for_rhyme
import random
import csv
import datetime
from wonderwords import RandomWord
import time
import numpy as np

LOG_INFO_DEBUG = "LOG/DEBUG: "
N_MATCH_MAX = 5


"""
全体の流れ
①ランダムに英単語を選択（品詞は、名詞・形容詞・動詞・副詞）
②言語をランダムに選択して、翻訳（Google Translateの回数制限に注意）
③翻訳した単語をIPA辞書を使って、IPAに変換
④ ③の単語の言語以外の言語でIPA辞書にマッチする単語を検索する
⑤ ③の単語と④のIPAマッチングした単語をCSVに書き込む
"""

def main():
    output = [["request_word", "request_lang", "request_pos", "request_ipa", "request_ipa_formatted", "request_word_en",
               "response_word", "response_lang", "response_pos", "response_ipa", "response_ipa_formatted",
               "response_word_en", ]]
    count = 0
    N = 1000

    # 翻訳クラスのインスタンス化
    translate = Translate()
    # IPA変換→マッチング処理のインスタンス化
    ipaMatchWordSearcher = IpaMatchWordSearcher()
    # トークナイザーのインスタンス化
    tokenize = TokenizerSpacy()

    r = RandomWord()

    for i in range(N):
        random_word_pos = ""
        request_word = "Apple"

        """ 以下の場合、再取得する
        ① 固有名詞の時
        ② tokenizerの結果、品詞情報が得られなかった時
        ③ ※ 名詞だった時（名詞は動詞、形容詞に比べて３倍近い個数存在するので、品詞の偏りが出ないように70%の確率で却下する 参考：http://user.keio.ac.jp/~rhotta/hellog/2012-06-02-1.html
        """
        isAccept = False
        while request_word[0].isupper() \
                or random_word_pos == "" \
                or (random_word_pos == "noun" and isAccept is True):
            try:
                ## TODO: 副詞も含めて、ランダムな英単語を取得するライブラリを探す or 自作する
                request_word = r.word(include_parts_of_speech=["verbs", "adjectives"], word_max_length=10)

                print(request_word)
                if request_word is None:
                    continue
                random_word_pos = tokenize.fetch_target_pos(word=request_word, word_en=request_word, lang="en")
                if random_word_pos == "noun":
                    isAccept = random.choices([True, False], weights=[0.3, 0.7], k=1)
            except Exception:
                pass
        print(LOG_INFO_DEBUG + "request word selected!!!!")
        print(LOG_INFO_DEBUG + "request_word:" + request_word)

        langs = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro', 'ar', 'is', 'vi', 'sv', 'fr', 'fi']
        # ランダムに並び替えて初期化
        random.shuffle(langs)

        """
        googleのtranslateのapiに回数制限があるので、
        全ての言語ではなく、シャッフルした上で先頭7個の言語にtranslateする（※ 7個は適当な値）
        """
        for j, lang in enumerate(langs[:7]):
            print(LOG_INFO_DEBUG + str(i) + "-" + str(j))

            request_word_lang = lang
            print(LOG_INFO_DEBUG + "start translating request word: " + str(request_word_lang))
            request_word_translated = translate.translate_by_language(word=request_word, lang=request_word_lang)
            print(
                LOG_INFO_DEBUG + f"finish translating request adjective word = {request_word_translated}, lang = {request_word_lang}")

            # create request_word_pos
            request_word_pos = tokenize.fetch_target_pos(word=request_word_translated, word_en=request_word,
                                                         lang=request_word_lang)
            if request_word_pos == "" or request_word_pos == "noun":
                continue

            """
            IPA変換→マッチング処理
            TODO: IPAConverterの命名：処理の中にマッチング処理も含めてるので、メソッドなりクラスを分けてもいいかも
            """
            print(LOG_INFO_DEBUG + "start ipa search for request word")
            response_dict = ipaMatchWordSearcher.execute(word=request_word_translated, lang=request_word_lang)
            response_word = response_dict["word_vowel_matched"]
            response_word_lang = response_dict["lang_vowel_matched"]
            response_word_pos = response_dict["word_vowel_matched_pos"]

            if response_word == "":
                print(LOG_INFO_DEBUG + f"not found ipa matched word ")
                continue
            print(
                LOG_INFO_DEBUG + f"finish ipa search for request adjective word/  response_word={response_word}, response_word_lang={response_word_lang}, response_word_pos={response_word_pos}")

            print()
            # request
            tmp = []

            print(LOG_INFO_DEBUG + "start writing tmp list to output")
            # write request info
            # -- preprocessing
            request_word_ipa = ipaMatchWordSearcher.convert_to_ipa(word=request_word_translated, lang=request_word_lang)

            # -- request
            tmp.append(request_word_translated)
            tmp.append(request_word_lang)
            tmp.append(request_word_pos)
            tmp.append(request_word_ipa)
            tmp.append(new_format_for_ipa_rhyme(convert_to_target_vowels_consonents_for_rhyme(request_word_ipa)))
            tmp.append(translate.translate_to_english_by_language(word=request_word_translated, lang=request_word_lang))

            # write response info
            # -- preprocessing
            response_word_ipa = ipaMatchWordSearcher.convert_to_ipa(word=response_word, lang=response_word_lang)

            # --  response
            tmp.append(response_word)
            tmp.append(response_word_lang)
            tmp.append(response_word_pos)
            tmp.append(response_word_ipa)
            tmp.append(new_format_for_ipa_rhyme(convert_to_target_vowels_consonents_for_rhyme(response_word_ipa)))
            tmp.append(translate.translate_to_english_by_language(word=response_word, lang=response_word_lang))

            # jsonに書き込み
            output.append(tmp)
            print(LOG_INFO_DEBUG + "=======================================================================")
            print(LOG_INFO_DEBUG + f"{tmp}")
            print(LOG_INFO_DEBUG + "=======================================================================")
            print(LOG_INFO_DEBUG + f"now progres searching, write tmp list to output current count: {count}")

    print(LOG_INFO_DEBUG + "start writing output to csv")
    f = open('../output/spacy_match-word-augumentation/' + str(datetime.datetime.now().time()) + '_otameshi.csv', 'w')
    write = csv.writer(f)
    write.writerows(output)
    print(LOG_INFO_DEBUG + f"finish writing output to csv/ {len(output)}")


if __name__ == "__main__":
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
