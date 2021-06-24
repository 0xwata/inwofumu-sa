import pandas as pd
import glob

request_column = ["request_word","request_lang","request_pos","request_ipa","request_ipa_formatted","request_word_en"]
response_column = ["response_word","response_lang","response_pos","response_ipa","response_ipa_formatted","response_word_en"]

request_column_rename_dict = {
    "request_word":"word",
    "request_lang":"word_lang",
    "request_pos":"word_pos",
    "request_ipa":"word_ipa",
    "request_ipa_formatted":"word_ipa_edited_vowel",
    "request_word_en":"word_en"
}
response_column_rename_dict = {
    "response_word":"word",
    "response_lang":"word_lang",
    "response_pos":"word_pos",
    "response_ipa":"word_ipa",
    "response_ipa_formatted":"word_ipa_edited_vowel",
    "response_word_en":"word_en"
}

def create_df():
    files = glob.glob("../output/spacy/*.csv")
    for i, file in enumerate(files):
        if i == 0:
            df = pd.read_csv(file, sep=',')
            print(f"count={i}")
            continue
        df_tmp = pd.read_csv(file, sep=',')
        df = pd.concat([df, df_tmp])
        print(f"count={i}")
    print(f"len(df)={len(df)}")

    # # 品詞が同じIPAペアを抽出
    # df_pos_matched = df[df.request_pos == df.response_pos]
    # print(f"len(df)={len(df_pos_matched)}")

    return df


df = pd.read_csv("../output/final/3447_spacy.csv", sep=',', index_col=0)
print(df.groupby('word_pos').size())

df_spacy = create_df()
requests = df_spacy[request_column]
requests_renamed = requests.rename(columns=request_column_rename_dict)

responses = df_spacy[response_column]
responses_renamed =responses.rename(columns=response_column_rename_dict)

df_concat = pd.concat([requests_renamed, responses_renamed])
df_concat_d = df_concat[~df_concat.duplicated()]
df_concat_d_r = df_concat_d.reset_index(drop=True)
print(df_concat_d_r.groupby('word_pos').size())





