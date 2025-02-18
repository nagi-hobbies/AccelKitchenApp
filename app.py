import streamlit as st


def main():
    page_home = st.Page("src/pages/home.py", title="Home", icon=":material/house:")
    page_cw_change_date = st.Page(
        "src/pages/cosmicwatch/change_date.py",
        title="日付の変更",
        icon=":material/calendar_today:",
    )
    pg = st.navigation(
        {
            "": [page_home],
            "CosmicWatch": [page_cw_change_date],
        }
    )

    pg.run()


if __name__ == "__main__":
    main()
