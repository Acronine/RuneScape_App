from tomongo import ToMongo
import pandas as pd
import requests, json
import base64
import streamlit as st


class RuneScapeEngine(ToMongo):
    """
    This object inherits from the ToMongo class. This is primarily to be able
    to directly query from the Mongo database. The purpose of this object is
    when initiated, the class will query the data in real time to give the user
    the most up to date information.

    The attributes of this class are:
        -Header GE: Dictionary; This is the unique user agent used to gain
            access into the RuneScape Wiki Api, primarily used in the
            class's initiation.
        -Header Price: Dictionary; The unique user agent used when querying
        the price history.
        -cdf: Data Frame; New data frame object from the queried data off of
            MongoDB and concatenating real time prices into the data frame.
        -Bond Value: Integer; Taking the average sell price of RuneScape Bonds
            and dividing the USD price ($6.99) by the that sell price, I get
            the value of 1 Gold Piece to USD. This is used to calculate real
            world trade value of items.
        -(H)igh (A)lchemy Price: This is the current average price of a nature
            rune. This is used to calculate the profit of casting high alchemy
            due to it costing one nature rune per cast.
    The method of this class is:
        -Autoplay Audio: auto plays music when the user goes to a page.
            There is no functionality currently in Streamlit to auto play
            music. The Streamlit Admin Zachary Blackwood shared this function
            online to do this.
    """
    # Unique user-agents to help give the RuneScape Wiki an idea
    #  what I'm using their api for.
    header_ge = {
        'User-Agent': 'Initiating a class to locally query data',
        'From': "@TheFirmPenguin#8408"
        }
    header_price = {
        'User-Agent': 'Querying individual item prices to display to the user',
        'From': "@TheFirmPenguin#8408"
    }

    def __init__(self):
        # Querying all the current prices once.
        inform = requests.get(
            r"https://prices.runescape.wiki/api/v1/osrs/latest",
            headers=self.header_ge).json()
        # Indexing into the json to reduce repetitive typing.
        dirty_df = inform['data']
        # Initiating the ToMongo class to connect to the server.
        ToMongo.__init__(self)
        # Querying the data off the server and setting it to a data frame.
        cursor = self.runescape_items.find()
        self.cdf = pd.DataFrame(list(cursor))
        # Creating the bond value and high alchemy price to be used for later.
        self.bond_value = 6.99 / ((
            dirty_df["13190"]['high'] +
            dirty_df["13190"]['low']) / 2)
        self.ha_price = round((
            dirty_df["561"]['high'] +
            dirty_df["561"]['low']) / 2, 0)
        # Creating three new columns to add onto the data frame.
        item_price = []
        true_value = []
        high_alch = []
        for i in range(len(self.cdf['id'])):
            item_id = self.cdf['id'][i]
            """
            When a item hasn't been traded for over 24 hours, the api sets its
            value to zero, this will rarely happen because of the amount of
            trading that goes on in RuneScape. However, the items most likely
            to not be traded would be the 3rd age set due to their insane
            scarcity. To account for this, I use a try & except to catch any
            of these and set the price to 0.
            """
            try:
                item_price.append(int(round((
                    dirty_df[f"{item_id}"]['high'] +
                    dirty_df[f"{item_id}"]['low']) / 2, 0)))
                true_value.append(round(item_price[i] * self.bond_value, 2))
                high_alch.append(
                    self.cdf['highalch'][i] - item_price[i] - self.ha_price
                    )
            except:
                item_price.append(0)
                true_value.append(0)
                high_alch.append(
                    self.cdf['highalch'][i] - item_price[i] - self.ha_price
                    )
        # Adding the new columns to the original data frame.
        self.cdf["ge_price"] = item_price
        self.cdf['usd_value'] = true_value
        self.cdf['ha_profit'] = high_alch
        # Dropping the _id column that was created when sending into the DB.
        self.cdf.drop(columns="_id", inplace=True)
        
    @staticmethod
    def autoplay_audio(file_path: str):
        """
        Auto plays the music in the streamlit app. Function built by Streamlit
        Admin Zachary Blackwood.
        """
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true">
                <source src="data:audio/ogg;base64,{b64}" type="audio/ogg">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )
        
if __name__ == "__main__":
    c = RuneScapeEngine()
    print(c.cdf)
    print(c.ha_price)