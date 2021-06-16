from adjective_noun_pair import AdjectiveNounPairSelector
from translate import Translate
from ipa_match_word_searcher import IpaMatchWordSearcher
import random
import csv
import datetime

LOG_INFO_DEBUG = "LOG/DEBUG: "


def execute():
    output = [["request_noun_word", "request_noun_lang", "request_noun_word_en","request_noun_ipa",
                "response_noun_word", "response_noun_lang","response_noun_word_en","response_noun_ipa"]]
    count = 0
    N = 100

    for i in range(N):
        langs = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro']

        noun_index = list(range(7))

        # ランダムに並び替えて初期化
        random.shuffle(noun_index)
        print(LOG_INFO_DEBUG + f"{noun_index}")

        # 名詞・形容詞のランダム取得クラスのインタンス化
        adjective_noun_pair_selector = AdjectiveNounPairSelector()
        # 名詞の取得
        request_noun = adjective_noun_pair_selector.fetch_random_noun()

        print(LOG_INFO_DEBUG + "request-noun:" + request_noun)

        for j in range(7):
            print(LOG_INFO_DEBUG + str(i) + "-" + str(j))

            # 翻訳クラスのインスタンス化
            translate = Translate()

            # 名詞のIPA変換→マッチング処理のインスタンス化
            ipa_converter = IpaMatchWordSearcher()

            print(LOG_INFO_DEBUG + "start translating request noun word")
            request_target_noun_lang = langs[noun_index[j]]
            request_noun_word_translated = translate.translate_by_language(word=request_noun,
                                                                           lang=request_target_noun_lang)
            print(
                LOG_INFO_DEBUG + f"finish translating request noun word/ word = {request_noun_word_translated}, lang = {request_target_noun_lang}")

            print()

            """
            名詞のIPA変換→マッチング処理
            """
            print(LOG_INFO_DEBUG + "start ipa search for request noun word")
            response_noun_word, response_noun_lang = ipa_converter.execute(word=request_noun_word_translated,lang=request_target_noun_lang, pos="NN")
            if response_noun_word == "":
                print(LOG_INFO_DEBUG + f"not found ipa matched noun word ")
                continue
            print(
                LOG_INFO_DEBUG + f"finish ipa search for request noun word/  word={response_noun_word}, lang={response_noun_lang}")

            print()
            # request
            tmp = []

            print(LOG_INFO_DEBUG + "start writing tmp list to output")
            # write request info
            # -- noun
            tmp.append(request_noun_word_translated)
            tmp.append(request_target_noun_lang)
            tmp.append(translate.translate_to_english_by_language(word=request_noun_word_translated,lang=request_target_noun_lang))
            tmp.append(ipa_converter.convert_to_ipa(word=request_noun_word_translated, lang=request_target_noun_lang))

            # write response info
            # -- noun
            tmp.append(response_noun_word)
            tmp.append(response_noun_lang)
            tmp.append(translate.translate_to_english_by_language(word=response_noun_word, lang=response_noun_lang))
            tmp.append(ipa_converter.convert_to_ipa(word=response_noun_word, lang=response_noun_lang))

            # jsonに書き込み
            output.append(tmp)
            print(LOG_INFO_DEBUG + "=======================================================================")
            print(LOG_INFO_DEBUG + f"{tmp}")
            print(LOG_INFO_DEBUG + "=======================================================================")
            print(LOG_INFO_DEBUG + f"now progres searching, write tmp list to output current count: {count}")


    print(LOG_INFO_DEBUG + "start writing output to csv")
    f = open('../output/noun-pair/' + str(datetime.datetime.now().time()) + '.csv', 'w')
    write = csv.writer(f)
    write.writerows(output)
    print(LOG_INFO_DEBUG + f"finish writing output to csv/ {len(output)}")

