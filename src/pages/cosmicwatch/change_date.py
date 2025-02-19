import datetime

import pandas as pd
import streamlit as st

import src.lib.cosmicwatch as cw

st.header("CosmicWatch 日付の変更", divider=True)

file = st.file_uploader("日付を変更するファイルをアップロード", type=["dat", "txt"])

if file is not None:
    df = cw.CosmicWatchAnalysis.read_file(file)

    with st.expander("変更前のデータ"):
        st.write("最初の5行")
        st.write(df.head())
        st.write("最後の5行")
        st.write(df.tail())

    start_date = st.date_input("開始日を入力してください")
    start_time = st.time_input("開始時間を入力してください")
    name = st.text_input("ファイル名を入力してください")

    full_date = datetime.datetime.combine(start_date, start_time)
    file_name = f"{name}_{full_date.strftime('%Y%m%d%H%M')}.{file.name.split('.')[-1]}"

    st.write(f"ファイル名: {file_name}")

    if st.button(label="日付を変更する"):
        with st.spinner("日付を変更しています..."):
            df = cw.CosmicWatchAnalysis.change_date(df, full_date)

            with st.expander("変更後のデータ"):
                st.write("最初の5行")
                st.write(df.head())
                st.write("最後の5行")
                st.write(df.tail())

            st.download_button(
                label="変更後のファイルをダウンロード",
                data=df.to_csv(sep="\t", index=False, header=False).encode(),
                file_name=file_name,
                mime="text/csv",
            )
        st.success("日付の変更が完了しました。")
