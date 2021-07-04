
import pandas as pd
import glob
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time


url = "https://linguatools-english-collocations.p.rapidapi.com/bolls/"

# .envファイルの内容を読み込みます
load_dotenv()

headers = {
    'x-rapidapi-key': os.environ['X-RAPIDAPI-KEY'],
    'x-rapidapi-host': os.environ['X-RAPIDKEY-HOST']
}

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

def fetch_response(word: str) -> list:
    querystring = {"lang":"en","query":word, "max_results":"10000", "min_sig":"0"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.encoding = response.apparent_encoding  # この行を追加

    return response.json()


def modify_df(df):
    requests = df[request_column]
    requests_renamed = requests.rename(columns=request_column_rename_dict)

    responses = df[response_column]
    responses_renamed =responses.rename(columns=response_column_rename_dict)

    df_concat = pd.concat([requests_renamed, responses_renamed])
    df_concat_d = df_concat[~df_concat.duplicated()]
    df_concat_d_r = df_concat_d.reset_index(drop=True)
    print(len(df_concat_d_r))
    print(df_concat_d_r.groupby('word_pos').size())

    return df_concat_d_r

def query_formatter(query):
    print(">"+query+"<")
    query = query.lower()

    if query.startswith('to '):
        query = query[3:]
    elif query.startswith('be '):
        query = query[3:]
    elif query.startswith('a '):
        query = query[2:]


    if query.endswith('.'):
        print("endswith")
        query = query[:-1]

    return query


def main():

    dfs_screaning = pd.read_csv('../output/final/final/output_after_screaning.csv', index_col=0, chunksize=100)
    _dfs_screaning = pd.read_csv('../output/final/final/output_after_screaning.csv', index_col=0)
    N = len(_dfs_screaning)
    print(N)
    count = 0
    request_count = 0
    result = []
    """
    """
    for df_screaning in dfs_screaning:
        print(len(df_screaning))
        ## 最新のcollocationsファイルを読み込み
        df_collocations = pd.read_csv('../output/collocations/collocations.csv', index_col=0)
        words = df_collocations.word

        # df_concat_d_r = modify_df(df_screaning)

        result = []
        df_word_en = df_screaning.word_en
        for idx in range(df_screaning.shape[0]):
            query = df_word_en.iloc[idx]
            if type(query) == float:
                continue
            query_formatted = query_formatter(query)
            if query_formatted in words:
                continue
            request_count +=1
            response = fetch_response(query_formatted)
            print(idx, query_formatted, len(response))
            for row in response:
                tmp = []
                collocation_id = row["id"]
                collocation = row["collocation"]
                relation = row["relation"]
                tmp.append(query_formatted)
                tmp.append(collocation_id)
                tmp.append(collocation)
                tmp.append(relation)
                result.append(tmp)
            time.sleep(3)
        print(len(result))
        df_result = pd.DataFrame(result, columns=["word", "collocation_id", "collocation_word", "collocation_relation"])
        print(len(df_collocations), len(df_result))
        df_output = df_collocations.append(df_result)
        df_output_r = df_output.reset_index(drop=True)
        print(len(df_output_r), len(df_result))
        df_output_r.to_csv('../output/collocations/collocations_with_screaning.csv')
        time.sleep(5)


        print(f"count={count}/{N}")
        count += 1


if __name__ == "__main__":
    main()