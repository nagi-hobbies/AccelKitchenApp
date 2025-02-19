import streamlit as st


def main():
    page_home = st.Page("src/pages/home.py", title="Home", icon=":material/house:")
    page_cw_rough_plots = st.Page(
        "src/pages/cosmicwatch/rough_plots.py",
        title="かんたんグラフ作成",
        icon=":material/insert_chart_outlined:",
        url_path="cw_rough_plots",
    )
    page_cw_change_date = st.Page(
        "src/pages/cosmicwatch/change_date.py",
        title="日付の変更",
        icon=":material/calendar_today:",
        url_path="cw_change_date",
    )
    page_rp_rough_plots = st.Page(
        "src/pages/redpitaya/rough_plots.py",
        title="かんたんグラフ作成",
        icon=":material/insert_chart_outlined:",
        url_path="rp_rough_plots",
    )
    pg = st.navigation(
        {
            "": [page_home],
            "CosmicWatch": [page_cw_rough_plots, page_cw_change_date],
            "RedPitaya": [page_rp_rough_plots],
        }
    )

    pg.run()


if __name__ == "__main__":
    main()
