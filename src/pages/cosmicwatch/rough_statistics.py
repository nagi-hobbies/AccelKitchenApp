import numpy as np
import pandas as pd
import streamlit as st
from streamlit import session_state as state

import src.lib.cosmicwatch as cw

st.set_page_config(layout="wide")

st.header("かんたん統計解析", divider=True)

st.subheader("データの読み込み", divider=True)

file = st.file_uploader(
    "グラフを作成するファイルをアップロード", type=["dat", "txt"], key="file_uploader"
)

if file is not None and file != state.get("uploaded_file"):
    state.uploaded_file = file
    with st.spinner("ファイルを読み込んでいます...(数分かかる場合があります)"):
        df = cw.CosmicWatchAnalysis.read_file(file)
        state.df = df

if state.get("df") is not None:
    df = state.df

    st.subheader("全データ", divider=True)
    st.write(df)

    st.subheader("基本統計量", divider=True)
    st.write(df.describe())

    st.subheader("カウントレート", divider=True)

    whether_filter = st.checkbox("adcでフィルターする")
    adc_min = st.number_input(
        "adcの最小値",
        min_value=0,
        max_value=1023,
        value=0,
        disabled=not whether_filter,
    )
    adc_max = st.number_input(
        "adcの最大値",
        min_value=0,
        max_value=1023,
        value=1023,
        disabled=not whether_filter,
    )

    filtered_df = df[(df["adc"] >= adc_min) & (df["adc"] <= adc_max)]
    filtered_df["delta_t"] = filtered_df["totaltime"].diff()
    mean_delta_t = filtered_df["delta_t"].mean()
    countrate = 1 / mean_delta_t * 1000

    st.write(f"adcの範囲: {adc_min} ≦ adc ≦ {adc_max}")
    st.write(f"平均到来間隔[ms]: {mean_delta_t}")
    st.write(f"カウントレート[1/s]: {countrate}")

    with st.expander("フィルター後のデータ"):
        st.write(filtered_df)

    with st.expander("下のコードより前に一度だけ実行が必要なコード"):
        with open("src/assets/texts/cw_firstcell.txt", "r", encoding="utf-8") as f:
            first_cell_code = f.read()
        st.write("マウスホバー時に右上に表示されるコピーアイコンでコピーできます")
        st.code(first_cell_code)

    with st.expander("計算のためのpythonコード"):
        st.write("マウスホバー時に右上に表示されるコピーアイコンでコピーできます")
        st.code(
            f"df = CosmicWatchAnalysis.read_file('パスをコピー')\n"
            f"filtered_df = df[(df['adc'] >= {adc_min}) & (df['adc'] <= {adc_max})] # adcの条件を満たす行のみを抽出\n"
            f"filtered_df['delta_t'] = filtered_df['totaltime'].diff()\n # totaltimeの差分を取ることで、一つ前のイベントからの経過時間を計算、delta_t列として追加\n"
            f"mean_delta_t = filtered_df['delta_t'].mean()\n"
            f"countrate = 1 / mean_delta_t * 1000 # ms -> sのための*1000\n"
            f"print(f'平均到来間隔[ms]: {mean_delta_t}')\n"
            f"print(f'カウントレート[1/s]: {countrate}')"
        )
