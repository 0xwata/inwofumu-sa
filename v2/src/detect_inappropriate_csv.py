
import glob
import pandas as pd
from typing import Optional
import shutil



def main():
    """CSVの読み込み """
    input_base_url = "../output/deliverables/v2/"
    output_url = "../output/rhyme_pair/rhyme_pair.csv"

    files = glob.glob(f"{input_base_url}/*.csv")

    count = 0
    df_total = None
    for file in files:
        df = pd.read_csv(file)
        if len(df) < 15:
            print(file)
            shutil.move(file, "../output/deliverables/inappropriate/")
            count += 1
    print(f"count: len(files) = {count} / {len(files)}, = {count/len(files)}")


if __name__ == "__main__":
    main()