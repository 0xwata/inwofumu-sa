
import pandas
import pandas as pd
import numpy as np

def main():

    """CSVの読み込み """
    df = pandas.read_csv("../output/join_table/rhyme_table.csv")

    unique_pos_group = df["pos"].unique()
    unique_type_group = df["type"].unique()
    unique_rhyme_vowel_group = df["rhyme_vowel"].unique()
    unique_syllable_group = df["syllable"].unique()

    for unique_pos in unique_pos_group:
        for unique_type in unique_type_group:
            for unique_syllable in unique_syllable_group:
                for unique_rhyme_vowel in unique_rhyme_vowel_group:
                    tmp = df[(df["pos"] == unique_pos) & (df["type"] == unique_type) & (df["syllable"] == unique_syllable) & (df["rhyme_vowel"] == unique_rhyme_vowel)]
                    unique_word_group = pd.concat([tmp["word"], tmp["pair_word"]], axis=0).unique()
                    if len(unique_word_group) != 0:
                        np.savetxt(
                            f"../output/deliverables/{unique_rhyme_vowel}_{unique_type}_{unique_syllable}_{unique_pos}.csv",
                            unique_word_group,
                            delimiter=',',
                            fmt = "%s"
                        )


if __name__ == "__main__":
    main()