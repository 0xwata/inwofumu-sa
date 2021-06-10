from adjective_noun_pair import AdjectiveNounPairSelector
from translate import Translate
from ipa_match_word_searcher import IpaMatchWordSearcher
import json

def main():

    output = []
    N = 100

    """
    名詞・形容詞のランダム取得クラスのインタンス化
    """
    adjective_noun_pair_selector = AdjectiveNounPairSelector()

    """
    翻訳クラスのインスタンス化
    """
    translate = Translate()

    """
    形容詞・名詞のIPA変換→マッチング処理のインスタンス化
    """
    ipa_converter = IpaMatchWordSearcher()

    for i in range(N):

        """
        形容詞・名詞の取得
        """
        request_adjective = adjective_noun_pair_selector.fetch_random_adjective()
        request_noun = adjective_noun_pair_selector.fetch_random_noun()

        """
        形容詞・名詞の翻訳処理
        指定した７言語に翻訳
        """
        print()
        print("request-adjective:"+request_adjective)
        print("request-noun:"+request_noun)

        print("形容詞の翻訳開始")
        request_adjectives_translated = translate.translate_all_language(request_adjective)

        print("名詞の翻訳開始")
        request_nouns_translated = translate.translate_all_language(request_noun)

        """
        形容詞・名詞のIPA変換→マッチング処理
        """
        request_adjective, response_adjective  = ipa_converter.execute(words = request_adjectives_translated, pos="JJ")
        request_noun, response_noun  = ipa_converter.execute(words = request_adjectives_translated, pos="NN")

        request_dict = {
            "adjective" : request_adjective,
            "noun" : request_noun
        }
        response_dict = {
            "adjective" : response_adjective,
            "noun": response_noun
        }

        request_response_dict = {
            "request": request_dict,
            "response": response_dict
        }

    # jsonに書き込み
    output.append(request_response_dict)
    file_output = open('output.json','w')
    json.dump(output,file_output,indent=4) #ensure_ascii=False
    file_output.close()

if __name__ == "__main__":
    main()