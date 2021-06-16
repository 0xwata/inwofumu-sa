from adjective_noun_pair import AdjectiveNounPairSelector
from translate import Translate
from ipa_match_word_searcher import IpaMatchWordSearcher
import random
import csv
import datetime
import sys
import adjective_pair_search
import noun_pair_search

LOG_INFO_DEBUG = "LOG/DEBUG: "


def main():
    output = [["request_adjective_word", "request_adjective_lang", "request_adjective_word_en",
               "request_noun_word", "request_noun_lang", "request_noun_word_en",
               "response_adjective_word", "response_adjective_lang", "response_adjective_word_en",
               "response_noun_word", "response_noun_lang", "response_noun_word_en", ]]
    count = 0
    N = 100

    for i in range(N):
        langs = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro']
        adjective_index = list(range(7))

        noun_index = list(range(7))

        # ランダムに並び替えて初期化
        random.shuffle(adjective_index)
        random.shuffle(noun_index)
        print(LOG_INFO_DEBUG + f"{adjective_index}")
        print(LOG_INFO_DEBUG + f"{noun_index}")

        # 名詞・形容詞のランダム取得クラスのインタンス化
        adjective_noun_pair_selector = AdjectiveNounPairSelector()
        # 形容詞・名詞の取得
        request_adjective = adjective_noun_pair_selector.fetch_random_adjective()
        request_noun = adjective_noun_pair_selector.fetch_random_noun()

        print(LOG_INFO_DEBUG + "request adjective-noun pair selected!!!!")
        print(LOG_INFO_DEBUG + "request-adjective:" + request_adjective)
        print(LOG_INFO_DEBUG + "request-noun:" + request_noun)

        for j in range(7):
            print(LOG_INFO_DEBUG + str(i) + "-" + str(j))

            # 翻訳クラスのインスタンス化
            translate = Translate()

            # 形容詞・名詞のIPA変換→マッチング処理のインスタンス化
            ipa_converter = IpaMatchWordSearcher()

            print(LOG_INFO_DEBUG + "start translating request adjective word")
            request_target_adjective_lang = langs[adjective_index[j]]
            request_adjective_word_translated = translate.translate_by_language(word=request_adjective,
                                                                                lang=request_target_adjective_lang)
            print(
                LOG_INFO_DEBUG + f"finish translating request adjective word = {request_adjective_word_translated}, lang = {request_target_adjective_lang}")

            print(LOG_INFO_DEBUG + "start translating request noun word")
            request_target_noun_lang = langs[noun_index[j]]
            request_noun_word_translated = translate.translate_by_language(word=request_noun,
                                                                           lang=request_target_noun_lang)
            print(
                LOG_INFO_DEBUG + f"finish translating request noun word/ word = {request_noun_word_translated}, lang = {request_target_noun_lang}")

            print()

            """
            形容詞・名詞のIPA変換→マッチング処理
            """
            print(LOG_INFO_DEBUG + "start ipa search for request adjective word")
            response_adjective_word, response_adjective_lang = ipa_converter.execute(word=request_adjective_word_translated, lang=request_target_adjective_lang, pos="JJ")
            if response_adjective_word == "":
                print(LOG_INFO_DEBUG + f"not found ipa matched adjective word ")
                continue
            print(LOG_INFO_DEBUG + f"finish ipa search for request adjective word/  word={response_adjective_word}, lang={response_adjective_lang}")
            print(LOG_INFO_DEBUG + "start ipa search for request noun word")
            response_noun_word, response_noun_lang = ipa_converter.execute(word=request_noun_word_translated,lang=request_target_noun_lang, pos="NN")
            if response_noun_word == "":
                print(LOG_INFO_DEBUG + f"not found ipa matched noun word ")
                continue
            print(
                LOG_INFO_DEBUG + f"finish ipa search for request adjective word/  word={response_noun_word}, lang={response_noun_lang}")

            if response_adjective_word == "" or response_noun_word == "":
                continue

            print()
            # request
            tmp = []

            print(LOG_INFO_DEBUG + "start writing tmp list to output")
            # write request info
            # -- adjective
            tmp.append(request_adjective_word_translated)
            tmp.append(request_target_adjective_lang)
            tmp.append(translate.translate_to_english_by_language(word=request_adjective_word_translated,
                                                                  lang=request_target_adjective_lang))
            tmp.append(ipa_converter.convert_to_ipa(word=request_adjective_word_translated, lang=request_target_adjective_lang))
            # -- noun
            tmp.append(request_noun_word_translated)
            tmp.append(request_target_noun_lang)
            tmp.append(translate.translate_to_english_by_language(word=request_noun_word_translated,lang=request_target_noun_lang))
            tmp.append(ipa_converter.convert_to_ipa(word=request_noun_word_translated, lang=request_target_noun_lang))

            # write response info
            tmp.append(response_adjective_word)
            tmp.append(response_adjective_lang)
            tmp.append(translate.translate_to_english_by_language(word=response_adjective_word, lang=response_adjective_lang))
            tmp.append(ipa_converter.convert_to_ipa(word=response_adjective_word, lang=response_adjective_lang))

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
    f = open('../output/' + str(datetime.datetime.now().time()) + '.csv', 'w')
    write = csv.writer(f)
    write.writerows(output)
    print(LOG_INFO_DEBUG + f"finish writing output to csv/ {len(output)}")


if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) == 2:
        if args[1] == 'adjective':
            print("a")
            adjective_pair_search.execute()
        elif args[1] == 'noun':
            print("b")
            noun_pair_search.execute()
        else:
            print("argument is not appropriate")
    else:
        main()
