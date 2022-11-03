# -*- coding: utf-8 -*-

import pandas
import pandas as pd
import numpy as np

def main():
    df = pandas.read_csv("../output/rhyme_pair/rhyme_pair.csv")
    unique_pos_group = df["pos"].unique()
    unique_type_group = df["rhyme_type"].unique()
    unique_ipa_rhyme_group = df["match_ipa_rhyme"].unique()
    unique_syllable_group = df["syllable"].unique()

    count = 0
    over_row_length_threshold_count = 0
    row_length_threshold = 15
    for unique_pos in unique_pos_group:
        for unique_type in unique_type_group:
            for unique_syllable in unique_syllable_group:
                for unique_ipa_rhyme in unique_ipa_rhyme_group:
                    tmp = df[(df["pos"] == unique_pos) & (df["rhyme_type"] == unique_type) & (
                                df["syllable"] == unique_syllable) & (df["match_ipa_rhyme"] == unique_ipa_rhyme)]
                    tmp_word = tmp[["word", "word_lang", "word_en", "word_ja", "word_ipa_rhyme"]]
                    tmp_pair_word = tmp[["pair_word", "pair_word_lang", "pair_word_en", "pair_word_ja", "pair_word_ipa_rhyme"]]
                    tmp_pair_word.columns = ["word", "word_lang", "word_en", "word_ja", "word_ipa_rhyme"]
                    word_group = pd.concat([tmp_word, tmp_pair_word], axis=0)
                    unique_word_group = word_group.drop_duplicates(subset='word')
                    # print(unique_word_group)
                    if len(unique_word_group) >= row_length_threshold:
                        over_row_length_threshold_count += 1
                        file_name = '../output/deliverables/v2/{0}_{1}_{2}_{3}.csv'.format(unique_ipa_rhyme,unique_type, unique_syllable, unique_pos)
                        print(file_name, len(unique_word_group))
                        unique_word_group.to_csv(file_name, index=False)
                    count += 1
    print(f"{over_row_length_threshold_count} / {count}: {(over_row_length_threshold_count / count)*100} %")

    # """CSVの読み込み """
    # df = pandas.read_csv("../output/join_table/rhyme_table.csv")
    # unique_pos_group = df["pos"].unique()
    # unique_type_group = df["type"].unique()
    # unique_rhyme_vowel_group = df["rhyme_vowel"].unique()
    # unique_syllable_group = df["syllable"].unique()

    # count = 0
    # over_row_length_threshold_count = 0
    # row_length_threshold = 15
    # for unique_pos in unique_pos_group:
    #     for unique_type in unique_type_group:
    #         for unique_syllable in unique_syllable_group:
    #             for unique_rhyme_vowel in unique_rhyme_vowel_group:
    #                 tmp = df[(df["pos"] == unique_pos) & (df["type"] == unique_type) & (
    #                             df["syllable"] == unique_syllable) & (df["rhyme_vowel"] == unique_rhyme_vowel)]
    #                 tmp_word = tmp[["word", "word_lang", "word_en"]]
    #                 tmp_pair_word = tmp[["pair_word", "pair_word_lang", "pair_word_en"]]
    #                 tmp_pair_word.columns = ["word", "word_lang", "word_en"]
    #                 word_group = pd.concat([tmp_word, tmp_pair_word], axis=0)
    #                 unique_word_group = word_group.drop_duplicates(subset='word')
    #                 if len(unique_word_group) >= row_length_threshold:
    #                     over_row_length_threshold_count += 1
    #                     file_name = f'../output/deliverables/{unique_rhyme_vowel}_{unique_type}_{unique_syllable}_{unique_pos}.csv'
    #                     print(file_name, len(unique_word_group))
    #                     unique_word_group.to_csv(file_name, index=False)
    #                 count += 1
    # print(f"{over_row_length_threshold_count} / {count}: {(over_row_length_threshold_count / count)*100} %")

if __name__ == "__main__":
    main()
