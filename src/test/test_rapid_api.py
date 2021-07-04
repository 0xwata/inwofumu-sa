import requests
import os
from dotenv import load_dotenv
import pandas as pd

url = "https://linguatools-english-collocations.p.rapidapi.com/bolls/"

# .envファイルの内容を読み込みます
load_dotenv()

headers = {
    'x-rapidapi-key': os.environ['X-RAPIDAPI-KEY'],
    'x-rapidapi-host': os.environ['X-RAPIDKEY-HOST']
}

def fetch_response(word: str) -> list:
    querystring = {"lang":"en","query":word, "max_results":"10000", "min_sig":"0"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.encoding = response.apparent_encoding  # この行を追加

    return response.json()


def main():
    word = "blue"
    response = fetch_response(word)

    result = []
    tmp = []
    for row in response:
        collocation_id = row["id"]
        collocation = row["collocation"]
        relation = row["relation"]
        tmp.append(word)
        tmp.append(collocation_id)
        tmp.append(collocation)
        tmp.append(relation)
        result.append(tmp)
        tmp = []

    df = pd.DataFrame(result, columns=["word", "collocation_id", "collocation_word", "collocation_relation"])
    df.to_csv(f'../output/collocations/collocations_with_screaning.csv')
if __name__ == "__main__":
    main()