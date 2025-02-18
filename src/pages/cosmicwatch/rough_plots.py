import numpy as np
import pandas as pd
import streamlit as st
from streamlit import session_state as state

import src.lib.cosmicwatch as cw
import src.lib.rough_plots_generator as rpg

st.set_page_config(layout="wide")

st.header("かんたんグラフ作成", divider=True)

file = st.file_uploader(
    "グラフを作成するファイルをアップロード", type=["dat", "txt"], key="file_uploader"
)

if file is not None and file != state.get("uploaded_file"):
    state.uploaded_file = file
    with st.spinner("ファイルを読み込んでいます...(数分かかる場合があります)"):
        df = cw.CosmicWatchAnalysis.read_file(file)
        state.df = df
        state.rpg = rpg.RoughPlotsGenerator(df)

if state.get("df") is not None:
    df = state.df
    rpg = state.rpg

    with st.expander("データのプレビュー"):
        st.write("最初の5行")
        st.write(df.head())
        st.write("最後の5行")
        st.write(df.tail())

    st.divider()

    plot_type = st.selectbox(
        "プロットの種類", ["ヒストグラム", "散布図"], key="plot_type"
    )

    if plot_type == "ヒストグラム":
        column = st.radio(
            "列を選択してください", df.columns, horizontal=True, key="column"
        )
        cols_fig_size = st.columns(2)

        with st.sidebar:
            fig_width = st.slider(
                "グラフの幅", min_value=1, max_value=10, value=5, key="fig_width"
            )
            fig_height = st.slider(
                "グラフの高さ", min_value=1, max_value=10, value=4, key="fig_height"
            )

            title = st.text_input("グラフのタイトル", key="title")
            x_label = st.text_input("x軸のラベル", value=column, key="x_label")
            y_label = st.text_input("y軸のラベル", value="count", key="y_label")

        bins = st.slider("ビンの数", min_value=1, max_value=200, value=100, key="bins")

        cols_plot_config = st.columns(2, vertical_alignment="center", border=True)
        with cols_plot_config[0]:
            cols_x_lim = st.columns([1, 5, 5], vertical_alignment="center")
            with cols_x_lim[0]:
                x_lim_check = st.checkbox(
                    "x_lim_check", label_visibility="collapsed", key="x_lim_check"
                )
            with cols_x_lim[1]:
                x_lim_l = st.number_input(
                    "x軸の最小値",
                    value=df[column].min(),
                    disabled=not x_lim_check,
                    key="x_lim_l",
                )
            with cols_x_lim[2]:
                x_lim_u = st.number_input(
                    "x軸の最大値",
                    value=df[column].max(),
                    disabled=not x_lim_check,
                    key="x_lim_u",
                )
        with cols_plot_config[1]:
            cols_y_lim = st.columns([1, 5, 5], vertical_alignment="center")
            with cols_y_lim[0]:
                y_lim_check = st.checkbox(
                    "y_lim_check", label_visibility="collapsed", key="y_lim_check"
                )
            with cols_y_lim[1]:
                y_lim_l = st.number_input(
                    "y軸の最小値", value=0, disabled=not y_lim_check, key="y_lim_l"
                )
            with cols_y_lim[2]:
                y_lim_u = st.number_input(
                    "y軸の最大値", value=100, disabled=not y_lim_check, key="y_lim_u"
                )

        x_lim = (x_lim_l, x_lim_u) if x_lim_check else None
        y_lim = (y_lim_l, y_lim_u) if y_lim_check else None

        st.divider()

        fig = rpg.plot_histgram(
            df,
            column,
            figsize=(fig_width, fig_height),
            bins=bins,
            title=title,
            x_label=x_label,
            y_label=y_label,
            x_lim=x_lim,
            y_lim=y_lim,
        )
        st.pyplot(fig, use_container_width=False)
