import datetime

import pandas as pd
import streamlit as st


class CosmicWatchAnalysis:
    @staticmethod
    def read_file(file) -> pd.DataFrame:
        """
        ファイルを読み込み、データフレームに変換します。

        Args:
            file (io.BytesIO): 読み込むファイル

        Returns:
            pd.DataFrame: 整形されたデータフレーム
        """
        df = pd.read_csv(
            file,
            sep="\t",
            names=[
                "event",
                "date",
                "totaltime",
                "adc",
                "sipm",
                "deadtime",
                "temp",
                "hum",
                "pres",
            ],
        )
        # numeric columns
        df = df.apply(pd.to_numeric, errors="ignore")
        df["date"] = df["date"].apply(pd.to_datetime, format="%Y-%m-%d-%H-%M-%S.%f")

        return df

    @staticmethod
    def change_date(df: pd.DataFrame, start_date: datetime.datetime) -> pd.DataFrame:
        """
        データフレームの日付を変換します。

        Args:
            df (pd.DataFrame): 変換するデータフレーム
            start_date (str): 開始日付

        Returns:
            pd.DataFrame: 日付が変換されたデータフレーム
        """
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d-%H-%M-%S.%f")
        df["date"] = df["date"] + (start_date - df["date"].min())
        df["date"] = df["date"].dt.strftime("%Y-%m-%d-%H-%M-%S.%f")
        return df
