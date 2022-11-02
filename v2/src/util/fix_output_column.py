
import pandas as pd

## 列名：    word,word_lang,word_ipa,word_ipa_rhyme
## 列の中身： word,word_ipa, word_ipa_rhyme,lang
## になってるので変更したい
def main():
  output_column = ["word", "word_lang", "word_ipa",
               "word_ipa_rhyme", "word_en", "word_ja",
               "pair_word", "pair_word_lang", "pair_word_ipa",
               "pair_word_ipa_rhyme", "pair_word_en", "pair_word_ja",
               "rhyme_type", "match_ipa_rhyme", "pos", "syllable"
               ]

  df = pd.read_csv("../output/rhyme_pair/v2/b857717c-5a4a-11ed-ae8b-acde48001122.csv")
  tmp_word_lang = df["word_lang"] ## 実質 word_ipa
  tmp_word_ipa = df["word_ipa"] ## 実質 word_ipa_rhyme
  tmp_word_ipa_rhyme = df["word_ipa_rhyme"] ## 実質 lang

  df["word_lang"] = tmp_word_ipa_rhyme
  df["word_ipa"] = tmp_word_lang
  df["word_ipa_rhyme"] = tmp_word_ipa

  df.to_csv("../output/rhyme_pair/v2/fix-b857717c-5a4a-11ed-ae8b-acde48001122.csv", index=False)


if __name__ == "__main__":
    main()