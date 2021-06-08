from src.adjective_noun_pair import AdjectiveNounPairSelector
from src.

def main():
    """
    名詞・形容詞のランダム取得クラスのインタンス化
    """
    adjective_noun_pair_selector = AdjectiveNounPairSelector()

    """
    形容詞・名詞の取得
    """
    adjective: str = adjective_noun_pair_selector.fetch_random_adjective()
    noun: str = adjective_noun_pair_selector.fetch_random_noun()

    """
    翻訳クラスのインスタンス化
    """
    translate = Translate()

    """
    形容詞・名詞の翻訳処理
    """
    adjectives_translated = translate.translate_all_language(adjective)
    nouns_translated = translate.translate_all_language(noun)



    """
    形容詞・名詞のIPA変換→マッチング処理
    """
    ipa_converter = IpaMatchWordSearcher()
    ipa_converter.search(adjectives_translated)

    """
    マッチング済み単語の翻訳処理
    """

    """
    マッチング済み単語の品詞推定処理
    """

    """
    最終的なアウトプット
    [
        {
            request: {
                "adjective": {
                    "word":
                    "lang":
                },
                "noun": {
                    "word":
                    "lang":
                }
            },
            response: {
                "adjective": {
                    "word":
                    "lang":
                },
                "noun": {
                    "word":
                    "lang":
                }
            }
        }, ...
    ]
    """


if __name__ == "__main__":
    main()