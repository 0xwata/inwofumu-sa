from adjective_noun_pair import AdjectiveNounPairSelector
from translate import Translate
from ipa_match_word_searcher import IpaMatchWordSearcher
import random
import csv
import datetime

LOG_INFO_DEBUG = "LOG/DEBUG: "

def main():

    output = []
    output.append(["request_adjective_word", "request_adjective_lang", "request_adjective_word_en",
                "request_noun_word", "request_noun_lang", "request_noun_word_en",
                "response_adjective_word", "response_adjective_lang", "response_adjective_word_en",
                "response_noun_word", "response_noun_lang", "response_noun_word_en",])
    count = 0
    N = 100


    for i in range(N):
        langs = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'ru']
        adjective_index = list(range(7))

        noun_index = list(range(7))

        #ランダムに並び替えて初期化
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
        print(LOG_INFO_DEBUG + "request-adjective:" +request_adjective)
        print(LOG_INFO_DEBUG + "request-noun:"+request_noun)

        for i in range(7):

            # 翻訳クラスのインスタンス化
            translate = Translate()

            # 形容詞・名詞のIPA変換→マッチング処理のインスタンス化
            ipa_converter = IpaMatchWordSearcher()

            print(LOG_INFO_DEBUG + "start translating request adjective word")
            request_target_adjective_lang = langs[adjective_index[i]]
            request_adjective_word_translated = translate.translate_by_language(word=request_adjective, lang=request_target_adjective_lang)
            print(LOG_INFO_DEBUG + f"finish translating request adjective word = {request_adjective_word_translated}, lang = {request_target_adjective_lang}")

            print(LOG_INFO_DEBUG + "start translating request noun word")
            request_target_noun_lang = langs[noun_index[i]]
            request_noun_word_translated = translate.translate_by_language(word=request_noun, lang=request_target_noun_lang)
            print(LOG_INFO_DEBUG + f"finish translating request noun word/ word = {request_noun_word_translated}, lang = {request_target_noun_lang}")

            """
            形容詞・名詞のIPA変換→マッチング処理
            """
            print(LOG_INFO_DEBUG + "start ipa search for request adjective word")
            response_adjective_word, response_adjective_lang  = ipa_converter.execute_v2(word=request_adjective_word_translated, lang=request_target_adjective_lang, pos="JJ")
            if response_adjective_word == "":
                print(LOG_INFO_DEBUG + f"not found ipa matched adjective word ")
                continue
            print(LOG_INFO_DEBUG + f"finish ipa search for request adjective word/  word={response_adjective_word}, lang={response_adjective_lang}")
            print(LOG_INFO_DEBUG + "start ipa search for request noun word")
            response_noun_word, response_noun_lang  = ipa_converter.execute_v2(word=request_noun_word_translated, lang=request_target_noun_lang, pos="NN")
            if response_noun_word == "":
                print(LOG_INFO_DEBUG + f"not found ipa matched noun word ")
                continue
            print(LOG_INFO_DEBUG + f"finish ipa search for request adjective word/  word={response_noun_word}, lang={response_noun_lang}")

            if response_adjective_word == "" or response_noun_word == "":
                continue
            #request
            tmp = []

            print(LOG_INFO_DEBUG + "start writing tmp list to output")
            # write request info
            ## -- adjective
            tmp.append(request_adjective_word_translated)
            tmp.append(request_target_adjective_lang)
            tmp.append(translate.translate_to_english_by_language(word=request_adjective_word_translated, lang=request_target_adjective_lang))
            ## -- noun
            tmp.append(request_noun_word_translated)
            tmp.append(request_target_noun_lang)
            tmp.append(translate.translate_to_english_by_language(word=request_noun_word_translated, lang=request_target_noun_lang))

            # write response info
            tmp.append(response_adjective_word)
            tmp.append(response_adjective_lang)
            tmp.append(translate.translate_to_english_by_language(word=response_adjective_word, lang=response_adjective_lang))
            ## -- noun
            tmp.append(response_noun_word)
            tmp.append(response_noun_lang)
            tmp.append(translate.translate_to_english_by_language(word=response_noun_word, lang=response_noun_lang))

            # jsonに書き込み
            output.append(tmp)
            print(LOG_INFO_DEBUG + f"now progres searching, write tmp list to output current count: {count}")

            #TODO: 後で消す。正常に動くか見たいため1回のループで検証
            break
        #TODO: 後で消す。正常に動くか見たいため1回のループで検証
        break
    print(LOG_INFO_DEBUG + "start writing output to csv")
    f = open('../output/' + str(datetime.datetime.now().time()) + '.csv', 'w')
    write = csv.writer(f)
    write.writerows(output)
    print(LOG_INFO_DEBUG + f"finish writing output to csv/ {len(output)}")

if __name__ == "__main__":
    main()