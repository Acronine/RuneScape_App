import streamlit as st

st.set_page_config(
    page_title="AlchMaster Toolkit",
    page_icon="⚔",
    menu_items={
        "About": """This app was made using the RuneScape Wiki
        Api. If you have any comments or run into any issues, here
        is my github: \n\rhttps://github.com/Acronine"""
    }
    )

st.title("AlchMaster Toolkit")
st.image(r'https://oldschool.runescape.wiki/images/High_Level_Alchemy.gif?5e779')
st.header("Welcome to the AlchMaster Toolkit!")
st.text(
    """This application provides a range of tools and insights tailored for
    RuneScape players and enthusiasts. Explore the following pages to
    discover valuable information, optimize your gameplay, and gain a
    deeper understanding of the game's economy"""
    )
st.text("The following were used to create this app.")
st.text("""
>Streamlit
>Python
>MongoDB
>Pandas
>RuneScape Wiki Api
        """)
st.header("Here are the different pages of my application:")

st.subheader("Item Info")
st.text("Queries the selected item and its corresponding information.")
st.markdown("""The information fields displayed are:
            item name, item icon, description, membership status, item id,
            current Grand Exchange Price, its USD real world trade value*, the
            high alchemy profit**, vendor price, high alchemy gold return,
            low alchemy gold return, and buy limit. If the profit is
            positive and there is a buy limit greater than 0, a text will
            display at the bottom to tell you the max profit you can make.
            \n* Value is calculated by taking the $6.99 bond price and dividing
            the bond gold exchange price to get the USD to 1 gold piece rate.
            \n* High Alchemy Profit is calculated by taking the gold return on
            casting high alchemy on the item, and subtracting the item's
            Grand Exchange price and subtracting 1 nature rune's Grand
            Exchange price.
            """)

st.subheader("High Alchemy Margins")
st.text("Queries the top high alchemy profitable items currently on the GE.")

st.subheader("Price History")
st.text("Queries the selected items price history.")
st.markdown("""The graph shown shows the last 365 increments of the selected
            time and displays the item's average high price and average low
            price being sold at at each of those increments. So say if you
            have 24h selected, it will show you the last 365 days(24h) and the
            item's corresponding values at each increment. The range of where
            these increments lie can also be changed. And the graph can be
            split to show high and low average prices separately.""")

st.subheader("Summary")
st.markdown("""This page provides a comprehensive explanation 
        of the app's internal mechanisms and delves into the underlying 
        reasons for each design choice.""")