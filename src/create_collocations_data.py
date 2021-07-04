
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


def main():

    files = glob.glob("../output/spacy_match-word-augumentation/*.csv")
    print(files)
    target_search_files = []
    count = 0
    request_count = 0
    result = []
    """
    """
    for file_path in files:
        ## 最新のcollocationsファイルを読み込み
        df_collocations = pd.read_csv('../output/collocations/collocations.csv', index_col=0)
        words = df_collocations.word
        ## 最新の検索済みファイルのログを読み込み
        already_searched_file_record = open('../output/collocations/already_searched_file_record.txt', 'r')
        data_already_searched_file_record = already_searched_file_record.read()
        print(data_already_searched_file_record)
        already_searched_file_record.close()

        print(">" + data_already_searched_file_record + "<")
        if data_already_searched_file_record == "":
            print("none")
        data_already_searched_file_li = data_already_searched_file_record.split(",")

        if file_path in data_already_searched_file_li:
            continue
        df = pd.read_csv(file_path, sep=',')
        df_concat_d_r = modify_df(df)

        result = []
        df_word_en = df_concat_d_r.word_en
        for idx in range(df_concat_d_r.shape[0]):
            query = df_word_en.iloc[idx]
            if query in words:
                continue
            request_count +=1
            response = fetch_response(query)
            print(idx, query, len(response))
            for row in response:
                tmp = []
                collocation_id = row["id"]
                collocation = row["collocation"]
                relation = row["relation"]
                tmp.append(query)
                tmp.append(collocation_id)
                tmp.append(collocation)
                tmp.append(relation)
                result.append(tmp)
            time.sleep(3)
        print(len(result))
        print("collocation探索終了.対象ファイル: ", file_path)
        df_result = pd.DataFrame(result, columns=["word", "collocation_id", "collocation_word", "collocation_relation"])
        print(len(df_collocations), len(df_result))
        df_output = df_collocations.append(df_result)
        df_output_r = df_output.reset_index(drop=True)
        print(len(df_output_r), len(df_result))
        df_output_r.to_csv('../output/collocations/collocations.csv')

        f = open('../output/collocations/already_searched_file_record.txt', 'w')
        f.write(data_already_searched_file_record)
        f.close()


        if data_already_searched_file_record == "":
            data_already_searched_file_record += file_path
        else:
            data_already_searched_file_record += "," + file_path
        print(f"count={count}")
        count += 1


if __name__ == "__main__":
    main()