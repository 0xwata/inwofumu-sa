import pandas as pd
import glob

"""
input:
    request_word,
    request_lang,
    request_pos,
    request_ipa,
    request_ipa_formatted,
    request_word_en,
    response_word,
    response_lang,
    response_pos,
    response_ipa,
    response_ipa_formatted,
    response_word_en

output:
    word（例: 懒散）
    word_language（例: ch)
    word_pos
    word_ipa
    word_ipa_edited_vowel
    word_en(例: Lazy)
    word_translated_by_01(例: 省略)
    word_translated_by_02(例: 省略)
    word_translated_by_03(例: 省略)
    word_translated_by_04(例: 省略)
    next_word_index_verb(例: 145:14:231:31:1）
    next_word_index_noun(例: 145:14:231:31:1）
    next_word_index_adjective(例: 145:14:231:31:1）
"""
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

output_column = ["word", "word_lang", "word_pos", "word_ipa", "word_ipa_edited_vowel", "word_en", "next_word_index_verb", "next_word_index_noun", "next_word_index_adjective"]

N_MATCH = 3


def ipa_chain_aggregator():
    df = create_df()
    requests = df[request_column]
    requests_renamed = requests.rename(columns=request_column_rename_dict)

    responses = df[response_column]
    responses_renamed =responses.rename(columns=response_column_rename_dict)

    df_concat = pd.concat([requests_renamed, responses_renamed])
    print(df_concat.duplicated().sum())
    print(len(df_concat[~df_concat.duplicated()]))
    df_concat_d = df_concat[~df_concat.duplicated()]
    df_concat_d_r = df_concat_d.reset_index(drop=True)



    output_count = 0
    group_next_word_index_verb = []
    group_next_word_index_noun = []
    group_next_word_index_adjective = []
    for i, row_i in df_concat_d_r.iterrows():
        query_ipa_vowel = row_i.word_ipa_edited_vowel[-N_MATCH:]
        query_word = row_i.word
        query_lang = row_i.word_lang

        next_word_index_verb = []
        next_word_index_noun = []
        next_word_index_adjective = []
        match_count = 0
        for j, row_j in df_concat_d_r.iterrows():
            if row_j.word == query_word or row_j.word_lang == query_lang:
                continue

            if(row_j.word_ipa_edited_vowel[-N_MATCH:] == query_ipa_vowel):
                if(row_j.word_pos == "verb"):
                    next_word_index_verb.append(str(j))
                elif(row_j.word_pos == "adjective"):
                    next_word_index_adjective.append(str(j))
                else: # row_j.pos == noun
                    next_word_index_noun.append(str(j))
                match_count += 1

        if len(next_word_index_verb) >= 3 and \
           len(next_word_index_adjective) >= 3 and \
           len(next_word_index_noun) >= 3:

           print(f"match_count:{match_count}")
           print(f"match_count_verb:{len(next_word_index_verb)}")
           print(f"match_count_adjective:{len(next_word_index_adjective)}")
           print(f"match_count_noun:{len(next_word_index_noun)}")
        group_next_word_index_verb.append(":".join(next_word_index_verb))
        group_next_word_index_adjective.append(":".join(next_word_index_adjective))
        group_next_word_index_noun.append(":".join(next_word_index_noun))

        print(f"next i->{i+1}")

    df_concat_d_r["next_word_index_verb"] = group_next_word_index_verb
    df_concat_d_r["next_word_index_adjective"] = group_next_word_index_adjective
    df_concat_d_r["next_word_index_noun"] = group_next_word_index_noun
    df_concat_d_r[output_column]

    df_concat_d_r.to_csv(f'../output/final/{len(df_concat_d_r)}.csv')
    print(f"finish writing output to csv/ {len(df_concat_d_r)}")


def create_df():
    files = glob.glob("../output/*.csv")
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

if __name__ == "__main__":
    ipa_chain_aggregator()
