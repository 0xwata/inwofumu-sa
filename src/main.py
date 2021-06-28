from nltk import tokenize
from adjective_noun_pair import AdjectiveNounPairSelector
from tokenizer import Tokenizer, TokenizerSpacy
from translate import Translate
from ipa_match_word_searcher import IpaMatchWordSearcher, new_format_for_is_ipa_rhyme, convert_to_target_vowels_consonents_for_rhyme
import random
import csv
import datetime
from wonderwords import random_word
from random_word import RandomWords


LOG_INFO_DEBUG = "LOG/DEBUG: "
N_MATCH_MAX = 5


def main():
    output = [["request_word", "request_lang", "request_pos", "request_ipa", "request_ipa_formatted", "request_word_en",
               "response_word", "response_lang", "response_pos", "response_ipa", "response_ipa_formatted", "response_word_en",]]
    count = 0
    N = 100

    # 翻訳クラスのインスタンス化
    translate = Translate()
    # IPA変換→マッチング処理のインスタンス化
    ipa_converter = IpaMatchWordSearcher()
    # トークナイザーのインスタンス化
    tokenize = TokenizerSpacy()

    random_words = RandomWords()

    for i in range(N):
        random_word_pos = ""
        while random_word_pos == "" or random_word_pos == "noun":
            request_word = random_words.get_random_word(hasDictionaryDef="true", includePartOfSpeech="adjective,verb", maxLength=N_MATCH_MAX)
            if request_word is None:
                continue
            random_word_pos = tokenize.fetch_target_pos(word=request_word, word_en=request_word, lang="en")

        print(request_word)
        print(LOG_INFO_DEBUG + "request word selected!!!!")
        print(LOG_INFO_DEBUG + "request_word:" + request_word)

        langs = ['ja', 'en', 'de', 'id', 'zh-cn', 'ko', 'eo', 'es', 'ro']
        index = list(range(7))
        # ランダムに並び替えて初期化
        random.shuffle(index)

        for j in range(7):
            print(LOG_INFO_DEBUG + str(i) + "-" + str(j))

            print(LOG_INFO_DEBUG + "start translating request word")
            request_word_lang = langs[index[j]]
            request_word_translated = translate.translate_by_language(word=request_word,lang=request_word_lang)
            print(LOG_INFO_DEBUG + f"finish translating request adjective word = {request_word_translated}, lang = {request_word_lang}")

            # create request_word_pos
            request_word_pos = tokenize.fetch_target_pos(word=request_word_translated, word_en=request_word, lang=request_word_lang)
            if request_word_pos == "" or request_word_pos == "noun":
                continue

            """
            IPA変換→マッチング処理
            """
            print(LOG_INFO_DEBUG + "start ipa search for request word")
            response_dict = ipa_converter.execute(word=request_word_translated, lang=request_word_lang)
            response_word = response_dict["word_vowel_matched"]
            response_word_lang = response_dict["lang_vowel_matched"]
            response_word_pos = response_dict["word_vowel_matched_pos"]

            if response_word == "":
                print(LOG_INFO_DEBUG + f"not found ipa matched word ")
                continue
            print(LOG_INFO_DEBUG + f"finish ipa search for request adjective word/  response_word={response_word}, response_word_lang={response_word_lang}, response_word_pos={response_word_pos}")

            print()
            # request
            tmp = []

            print(LOG_INFO_DEBUG + "start writing tmp list to output")
            # write request info
            # -- preprocessing
            request_word_ipa = ipa_converter.convert_to_ipa(word=request_word_translated, lang=request_word_lang)

            # -- request
            tmp.append(request_word_translated)
            tmp.append(request_word_lang)
            tmp.append(request_word_pos)
            tmp.append(request_word_ipa)
            tmp.append(new_format_for_is_ipa_rhyme(convert_to_target_vowels_consonents_for_rhyme(request_word_ipa)))
            tmp.append(translate.translate_to_english_by_language(word=request_word_translated,lang=request_word_lang))

            # write response info
            # -- preprocessing
            response_word_ipa = ipa_converter.convert_to_ipa(word=response_word, lang=response_word_lang)

            # --  response
            tmp.append(response_word)
            tmp.append(response_word_lang)
            tmp.append(response_word_pos)
            tmp.append(response_word_ipa)
            tmp.append(new_format_for_is_ipa_rhyme(convert_to_target_vowels_consonents_for_rhyme(response_word_ipa)))
            tmp.append(translate.translate_to_english_by_language(word=response_word, lang=response_word_lang))

            # jsonに書き込み
            output.append(tmp)
            print(LOG_INFO_DEBUG + "=======================================================================")
            print(LOG_INFO_DEBUG + f"{tmp}")
            print(LOG_INFO_DEBUG + "=======================================================================")
            print(LOG_INFO_DEBUG + f"now progres searching, write tmp list to output current count: {count}")


    print(LOG_INFO_DEBUG + "start writing output to csv")
    f = open('../output/spacy_match-word-augumentation/' + str(datetime.datetime.now().time()) + '.csv', 'w')
    write = csv.writer(f)
    write.writerows(output)
    print(LOG_INFO_DEBUG + f"finish writing output to csv/ {len(output)}")


if __name__ == "__main__":
    main()
