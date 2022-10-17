import ipa
import pandas
# from googletrans import Translator
from hyphen import Hyphenator
from enum import Enum
from typing import Optional


INPUT_COLUMNS = [
    "word",
    "word_lang",
    "word_en",
    "word_pos",
    "predicted_pronunciation"
]

OUTPUT_COLUMNS = {
    "id",
    "word",
    "pair_id",
    "pair_word",
    "type",
    "rhyme_vowel",
    "pos",
    "syllable"
}


def find_rhyme_vowel(ipa_1: str, ipa_2: str, rhyme_type: RhymeType) -> Optional[string]:
    s_ipa_1 = IPAString(unicode_string=ipa_1)
    s_ipa_2 = IPAString(unicode_string=ipa_2)

    if rhyme_type == RhymeType.TOIN:
        """頭韻判定"""

        return None

    else:
        """脚韻判定"""
        return None


def main():
    """ Translatorクラスのインスタンスを生成 """
    # translator = Translator()

    """CSVの読み込み """
    df_raw = pandas.read_csv("../data/v1_output.csv", index_col=0)
    df = df_raw[INPUT_COLUMNS]

    """ 
    音節数を調べる(IPAの母音を元にカウントする)
    """
    syllable_count_list = []
    ipa_list = df["predicted_pronunciation"]
    for ipa in ipa_list:
        s_ipa = IPAString(unicode_string=ipa)
        vowels = s_ipa.vowels
        syllable_count = len(vowels)
        syllable_count_list.append(syllable_count)
    df["syllable"] = syllable_count_list

    """
    中間テーブル(rhyme_table)を作成する
    | id | word |pair_id | pair_word | type        | rhyme_vowel | pos  | syllable |
    | 19 | hoge |40      | fuga      | to or kyaku | ou          | noun | 3        |
    """
    count = 0
    output = []
    for i, row_i in df.iterrows():
        word_i = row_i["word"]
        pos_i = row_i["word_pos"]
        syllable_i = row_i["syllable"]
        ipa_i = row_i["predicted_pronunciation"]
        s_ipa_i = IPAString(unicode_string=ipa_i)

        df_matching_candidate = df[(df["word_pos"] == pos_i) & (df["syllable"] == syllable_i)]

        for j, row_j in df_matching_candidate:
            word_j = row_j["word"]
            if word_i == word_j:
                continue
            else:
                ipa_j = row_j["predicted_pronunciation"]
                s_ipa_j = IPAString(unicode_string=ipa_j)

                # 頭韻判定
                rhyme_vowel = find_ipa_match(ipa_i, ipa_j, RhymeType.TOIN)
                if rhyme_vowel is not None:
                    tmp = [count, i, word_i, j, word_j, RhymeType.TOIN.name, rhyme_vowel, pos_i, syllable_i]
                    output.append(tmp)
                # 脚韻判定
                rhyme_vowel = find_ipa_match(ipa_i, ipa_j, RhymeType.KYAKUIN)
                if rhyme_vowel:
                    tmp = [count, i, word_i, j, word_j, RhymeType.KYAKUIN.name, rhyme_vowel, pos_i, syllable_i]
                    output.append(tmp)

    """ 中間テーブル(rhyme_table)の出力 -> rhyme_table.csv"""
    f = open('../output/join_table/rhyme_table.csv', 'w')
    write = csv.writer(f)
    write.writerows(output)


if __name__ == "__main__":
    main()
