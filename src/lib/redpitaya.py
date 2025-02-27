import datetime

import numpy as np
import pandas as pd
import streamlit as st


class RedpitayaAnalysis:
    @staticmethod
    def read_file(file) -> pd.DataFrame:
        """
        ファイルを読み込み、データフレームに変換します。

        Args:
            file (io.BytesIO): 読み込むファイル

        Returns:
            pd.DataFrame: 整形されたデータフレーム
        """
        data = np.loadtxt(file, delimiter=",", dtype=str)
        df = pd.DataFrame(
            data,
            columns=[
                "totaltime",  # 測定開始からの経過時間
                "totaldeadtime",  # データの書き込みにかかった時間など、データの計測が停止していた時間の合計
                "ch1_sum",  # チャンネル1の電圧積算値
                "ch1_max",  # チャンネル1の電圧最大値
                "ch2_sum",  # チャンネル2の電圧積算値
                "ch2_max",  # チャンネル2の電圧最大値
            ],
        )
        # numeric columns
        df = df.apply(pd.to_numeric, errors="ignore")

        return df
