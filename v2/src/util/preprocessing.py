# -*- coding: utf-8 -*-

import pandas

def main():
    """ CSVの読み込み """
    df = pandas.read_csv("../../data/multi_results.csv", index_col=0)
    ipa_dict_df = pandas.read_csv("../../data/ipa_dict.csv", index_col=0)
    print(df.head(3))
    print(ipa_dict_df.head(3))

    index_list = df["Audio"].apply(lambda x: int(x.split("_")[0]))

    print(index_list[0])
    print(df["Word"][0])
    print(ipa_dict_df.iloc[index_list[0]]["word"])

    word_pos_list = []
    for index in index_list:
        word_pos = ipa_dict_df.iloc[index]["word_pos"]
        word_pos_list.append(word_pos)

    print(len(index_list))
    print(len(word_pos_list))

    df["Pos"] = word_pos_list
    df.to_csv("../../data/multi_results_pos.csv")


if __name__ == "__main__":
    main()