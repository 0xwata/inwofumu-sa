# -*- coding: utf-8 -*-

import sys
import argparse
import create_rhyme_pair

## WIP: 引数に応じて実行する/skipする手順を制御する


def main(
    is_execute_create_rhyme_pair: bool,
    is_execute_create_rhyme_table: bool,
    is_execute_create_deliverables: bool
):
    """
    ① 韻を踏むペアを探す
      input:
      output: output/join_table/rhyme_pair.csv
    """
    if is_execute_create_rhyme_pair:
        create_rhyme_pair.main()

    """
    ② 今回の展示で必要な韻を踏むペアの音節と脚韻・頭韻の情報を付加する
      input: output/join_table/rhyme_pair.csv
      output: output/join_table/rhyme_table.csv
    """
    if is_execute_create_rhyme_table:
        create_rhyme_table.main()

    """
    ③ 今回の展示で求められる成果物を生成する
      input: output/join_table/rhyme_table.csv
      output: output/deliverables/**.csv
    """
    if is_execute_create_deliverables:
        create_deliverables.main()


if __name__ == "__main__":
    # 最初にパーサーとしてArgumentParserオブジェクトを作成する
    psr = argparse.ArgumentParser(
        prog='プログラムの名',
        usage='プログラムの使い方',
        description='プログラムの説明'
    )

    psr.add_argument('-rhyme_pair', '--first', required=True, type=bool, help='rhyme_pairの関数を実行する必要があるか')
    psr.add_argument('-rhyme_table', '--second', required=True, type=bool, help='rhyme_tableの関数を実行する必要があるか')
    psr.add_argument('-deliverables', '--third', required=True, type=bool, help='deliverablesの関数を実行する必要があるか')

    # 受け取った引数を解析する
    args = psr.parse_args()
    main(
        is_execute_create_rhyme_pair=args.first,
        is_execute_create_rhyme_table=args.second,
        is_execute_create_deliverables=args.third
    )

"""
コード実行スニペット
python main.py -rhyme_pair False -rhyme_table  False -deliverables
"""