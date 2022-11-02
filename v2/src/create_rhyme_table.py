from numpy import deprecate
import pandas
from ipapy.ipastring import IPAString
from hyphen import Hyphenator
from model.rhyme_type import RhymeType
import csv
from util.find_syllable_count import find_syllable_count
from util.format_word_ipa import format_word_ipa
from util.find_rhyme_vowel import find_rhyme_vowel
from model.rhyme_type import RhymeType

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
    "word_vowel", # <-- デバッグ用
    "word_lang",
    "word_en",
    "pair_id",
    "pair_word",
    "pair_word_vowel", # <-- デバッグ用
    "pair_word_lang",
    "pair_word_en",
    "type",
    "rhyme_vowel",
    "pos",
    "syllable"
]

@deprecate(message="こちらのメソッドは不使用となります。create_rhyme_pairのメソッドに処理をまとめました")
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
            syllable_count = find_syllable_count(format_word_ipa(ipa))
        syllable_count_list.append(syllable_count)
    df["syllable"] = syllable_count_list

    """
    中間テーブル(rhyme_table)を作成する（id必要ないかも)
    | id | word | word_vowel | word_lang| word_en | word_ja | pair_id | pair_word | pair_word | type        | rhyme_vowel | pos  | syllable |
    | 19 | hoge | oe         | 40       | hoge    | ほげ     | 12      |fuga      | ua        | to or kyaku | ou          | noun | 3        |
    """
    count = 0
    error_count = 0
    output = []

    ## TODO: for文2回回さないで良いようにinputのcsvの再設計をする
    for i, row_i in df.iterrows():
        print("progress rate: ", count, "/", len(df), "success rate: ", (len(df) - error_count) / len(df) * 100, "%")
        count += 1
        word_i = row_i["word"]
        word_lang_i = row_i["word_lang"]
        word_en_i = row_i["word_en"]
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
                word_lang_j= row_j["word_lang"]
                word_en_j = row_j["word_en"]
                if word_i == word_j:  # 同一単語の場合はskip
                    continue
                else:
                    ipa_j = format_word_ipa(row_j["word_ipa"])
                    ipa_str_j = IPAString(unicode_string=ipa_j)

                    # まずは脚韻判定をする
                    rhyme_vowel_kyakuin = find_rhyme_vowel(str(ipa_str_i.vowels), str(ipa_str_j.vowels),
                                                           RhymeType.KYAKUIN)
                    if rhyme_vowel_kyakuin is not None:
                        tmp = [i, word_i, ipa_str_i.vowels,word_lang_i, word_en_i,  j, word_j, ipa_str_j.vowels, word_lang_j, word_en_j, RhymeType.KYAKUIN.value,
                               rhyme_vowel_kyakuin, pos_i, syllable_i]
                        output.append(tmp)
                    else:
                        # 次に頭韻判定をする
                        rhyme_vowel_toin = find_rhyme_vowel(str(ipa_str_i.vowels), str(ipa_str_j.vowels),
                                                            RhymeType.TOIN)
                        if rhyme_vowel_toin is not None:
                            tmp = [i, word_i, ipa_str_i.vowels, word_lang_i, word_en_i, j, word_j, ipa_str_j.vowels, word_lang_j, word_en_j, RhymeType.TOIN.value,
                                   rhyme_vowel_toin, pos_i, syllable_i]
                            output.append(tmp)

        except ValueError as e:
            error_count += 1
            print("ValueError:", e)
            print(word_i, word_j)
            print(ipa_i, ipa_j)
            print("")
            pass


    ## TODO: 必要であれば、事前に出力する中間テーブルに対して正規化をかける
    # output_pd = pd.DataFrame(output)
    # output_pd.columns = OUTPUT_COLUMNS


    """ 中間テーブル(rhyme_table)の出力 -> rhyme_table.csv"""
    f = open('../output/join_table/rhyme_table.csv', 'w')
    write = csv.writer(f)
    write.writerow(OUTPUT_COLUMNS)
    write.writerows(output)


if __name__ == "__main__":
    main()
