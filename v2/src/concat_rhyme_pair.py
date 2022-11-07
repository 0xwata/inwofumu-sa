# -*- coding: utf-8 -*-

import glob
import pandas as pd
from typing import Optional


def main():
    """CSVの読み込み """
    input_base_url = "../output/rhyme_pair/v3/"
    output_url = "../output/rhyme_pair/v3/rhyme_pair_v3.csv"

    files = glob.glob(f"{input_base_url}/*.csv")

    count = 0
    df_total = None
    for file in files:
        if count == 0:
            df_total = pd.read_csv(file)
        else:
            df = pd.read_csv(file)
            df_total = pd.concat([df_total, df], axis=0)
        count += 1

    df_total.to_csv(output_url, index=False)


if __name__ == "__main__":
    main()

