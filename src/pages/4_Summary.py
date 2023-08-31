import streamlit as st
import os
import sys
from pathlib import Path

st.set_page_config(
    page_title="Summary Page",
    page_icon="⚔",
    menu_items={
        "About": """This app was made using the RuneScape Wiki
        Api. If you have any comments or run into any issues, here
        is my github: \n\rhttps://github.com/Acronine"""
    }
    )
# Setting up the filepath to allow the app to pull from the directory.
filepath = os.path.join(Path(__file__).parents[1])
sys.path.insert(0, filepath)

# Importing RuneScapeEngine
from runescape_query_engine import RuneScapeEngine
# Initiating the RuneScapeEngine to be able to grab the auto play function.
c = RuneScapeEngine()
st.title("Summary")

# This function is to autoplay the selected song
c.autoplay_audio(r'src/Sea_Shanty_2.ogg')

st.text("""
        The purpose of this application is to create an dashboard using the
        RuneScape Wiki Api. The first steps to do this was pulling the data,
        cleaning the data, pushing the data to MongoDB. After, I created a
        virtual environment that will house all of my python installs and
        the application. Following, I query the data and run it through
        Streamlit. I then create an easily accessible application that allows
        the user to look up any item on the Grand Exchange and its
        corresponding info.

        In addition to the item's info, the next page allows the user to view
        the top 10 - 50 profitable items through casting high alchemy on
        bought items. Afterwards, the price history page lets the user
        view the price history of any item recently sold on the Grand Exchange.
        They can also change the time increments to view from the last 1,825 
        minutes to the last whole year of sales of the selected item as a line
        chart.
        """)

st.text("""I would like to give a special thanks to the RuneScape Wiki team for
        allowing me to use their api. Their discord is
        https://discord.gg/runescapewiki if you'd like to check them out.
        They've all been great with helping me with random issues. I would
        also like to give a shout out to the user Duralith for helping me out
        on a few issues.""")

st.image('https://logos-download.com/wp-content/uploads/2016/09/MongoDB_logo_Mongo_DB.png')
st.balloons()