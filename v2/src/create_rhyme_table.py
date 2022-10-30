import ipa
import pandas
from ipapy.ipastring import IPAString
from hyphen import Hyphenator
from typing import Optional
from model.rhyme_type import RhymeType
import csv

INPUT_COLUMNS = [
    "word",
    "word_lang",
    "word_en",
    "word_pos",
    "word_ipa",
    "predicted_pronunciation"
]

OUTPUT_COLUMNS = [
    "id",
    "word",
    "word_vowel",
    "pair_id",
    "pair_word",
    "pair_word_vowel",
    "type",
    "rhyme_vowel",
    "pos",
    "syllable"
]

"""
@param: ipa_str_vowels_1: IPAStringのObjectのプロパティであるvowels
@param; ipa_str_vowels_2: 〃
"""


def find_rhyme_vowel(ipa_str_vowels_1: str, ipa_str_vowels_2: str, rhyme_type: RhymeType) -> Optional[str]:
    rhyme_bowel = ""
    print(ipa_str_vowels_1, ipa_str_vowels_2)

    if len(ipa_str_vowels_1) > len(ipa_str_vowels_2):
        a = ipa_str_vowels_1
        b = ipa_str_vowels_2
        max_rhyme_length = len(b)
    else:
        a = ipa_str_vowels_2
        b = ipa_str_vowels_1
        max_rhyme_length = len(b)

    if rhyme_type == RhymeType.TOIN:
        """頭韻判定"""
        for i in range(max_rhyme_length):
            if i == 0:
                continue
            if b.startswith(a[:i + 1]) is True:
                rhyme_bowel += b[i]
            else:
                break
        # 空文字もしくは1文字しか合致しなかった場合は、Noneを返す
        if len(rhyme_bowel) == 0 or len(rhyme_bowel) == 1:
            return None
        else:
            return rhyme_bowel
    else:
        """脚韻判定"""
        for i in range(max_rhyme_length):
            if i == 0:
                continue
            if b.endswith(a[-1 * i:]) is True:  ## 後ろから1文字ずつ追加していって判定していく
                rhyme_bowel += b[-1 * i]
            else:
                break

        # 空文字もしくは1文字しか合致しなかった場合は、Noneを返す
        if len(rhyme_bowel) == 0 or len(rhyme_bowel) == 1:
            return None
        else:
            return rhyme_bowel[::-1]  ## 後ろから1文字ずつ追加しているので最後は反転して渡す


def format_word_ipa(ipa: str) -> str:
    result = ""
    for char in ipa:
        if char == "/" or char == "̠ ":
            continue
        result += char
    return result


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
    ipa_list = df["word_ipa"]
    for ipa in ipa_list:
        if type(ipa) != str:
            syllable_count = -1
        else:
            try:
                s_ipa = IPAString(unicode_string=format_word_ipa(ipa))
                vowels = s_ipa.vowels
                syllable_count = len(vowels)
            except ValueError as e:
                print(e)
                syllable_count = -1
        syllable_count_list.append(syllable_count)
    df["syllable"] = syllable_count_list

    """
    中間テーブル(rhyme_table)を作成する
    | id | word | word_vowel | pair_id | pair_word | pair_word | type        | rhyme_vowel | pos  | syllable |
    | 19 | hoge | oe         | 40      | fuga      | ua        | to or kyaku | ou          | noun | 3        |
    """
    count = 0
    error_count = 0
    output = []
    for i, row_i in df.iterrows():
        print("progress rate: ", count, "/", len(df), "success rate: ", (len(df) - error_count) / len(df) * 100, "%")
        count += 1
        word_i = row_i["word"]
        pos_i = row_i["word_pos"]
        syllable_i = row_i["syllable"]
        ipa_i = format_word_ipa(row_i["word_ipa"])

        try:
            ipa_str_i = IPAString(unicode_string=ipa_i)

            if syllable_i == 0:
                continue

            df_matching_candidate = df[(df["word_pos"] == pos_i) & (df["syllable"] == syllable_i)]

            for j, row_j in df_matching_candidate.iterrows():
                word_j = row_j["word"]
                if word_i == word_j:  # 同一単語の場合はskip
                    continue
                else:
                    ipa_j = format_word_ipa(row_j["word_ipa"])
                    ipa_str_j = IPAString(unicode_string=ipa_j)

                    # まずは脚韻判定をする
                    rhyme_vowel_kyakuin = find_rhyme_vowel(str(ipa_str_i.vowels), str(ipa_str_j.vowels),
                                                           RhymeType.KYAKUIN)
                    if rhyme_vowel_kyakuin is not None:
                        tmp = [i, word_i, ipa_str_i.vowels, j, word_j, ipa_str_j.vowels, RhymeType.KYAKUIN.name,
                               rhyme_vowel_kyakuin, pos_i, syllable_i]
                        output.append(tmp)
                    else:
                        # 次に頭韻判定をする
                        rhyme_vowel_toin = find_rhyme_vowel(str(ipa_str_i.vowels), str(ipa_str_j.vowels),
                                                            RhymeType.TOIN)
                        if rhyme_vowel_toin is not None:
                            tmp = [i, word_i, ipa_str_i.vowels, j, word_j, ipa_str_j.vowels, RhymeType.TOIN.name,
                                   rhyme_vowel_toin, pos_i, syllable_i]
                            output.append(tmp)

        except ValueError as e:
            error_count += 1
            print("ValueError:", e)
            print(word_i, word_j)
            print(ipa_i, ipa_j)
            print("")
            pass

    """ 中間テーブル(rhyme_table)の出力 -> rhyme_table.csv"""
    f = open('../output/join_table/rhyme_table.csv', 'w')
    write = csv.writer(f)
    write.writerow(OUTPUT_COLUMNS)
    write.writerows(output)


if __name__ == "__main__":
    main()
