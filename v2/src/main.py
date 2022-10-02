import ipa
import pandas
from googletrans import Translator
import nltk
import re
from part_of_speech import PartOfSpeech

def find_part_of_speech(word_en: str, lang: str) -> PartOfSpeech:
    morph = nltk.word_tokenize(word_en)
    pos = nltk.pos_tag(morph)
    pos_tag = pos[0][1]
    if re.search('JJ*', pos_tag):
        return PartOfSpeech.adj
    elif re.search('NN*', pos_tag):
        return PartOfSpeech.noun
    elif re.search('VB*', pos_tag):
        return PartOfSpeech.verb
    elif re.search('RB*', pos_tag):
        return PartOfSpeech.adv
    else:
        return PartOfSpeech.other


"""
@param: df
"""
def find_ipa_chain():


def main():
    # Translatorクラスのインスタンスを生成
    translator = Translator()

    """ CSVの読み込み """
    df = pandas.read_csv("../data/multi_results.csv", index_col=0)
    print(df.head(3))

    """ 正解率 """
    print(len(df[df["Result"] == True]) / len(df))

    """ 品詞抽出 """
    # TODO: 言語の情報が必要
    df_for_pos = df["Word", "Lang"]
    pos_list = []
    for row in df_for_pos.iterrows():
        word_translated = translator.translate(row["Word"], dest="en", src=row["Lang"])
        pos = find_part_of_speech(word_en=word_translated, lang="ch")
        pos_list.append(pos.name)
    df["pos"] = pos_list

    # TODO: 音節の抽出

    """ 韻ペアの抽出 
        品詞（名詞, 形容詞, 副詞）ごとにペアを抽出
    """
    ipa_list = df["Predicted_Pronunciation"]

    find_ipa_chain()


if __name__ == "__main__":
    main()
