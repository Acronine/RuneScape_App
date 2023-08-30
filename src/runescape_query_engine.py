from tomongo import ToMongo
import pandas as pd
import requests, json
import base64
import streamlit as st

class RuneScapeEngine(ToMongo):
    # Unique user-agents to help give the RuneScape Wiki an idea
    #  what I'm using their api for.
    header = {
        'User-Agent': 'Initiating a class to locally query data',
        'From': "@TheFirmPenguin#8408"
        }

    def __init__(self):
        inform = requests.get(
            r"https://prices.runescape.wiki/api/v1/osrs/latest",
            headers=self.header).json()
        dirty_df = inform['data']
        ToMongo.__init__(self)
        cursor = self.runescape_items.find()
        self.cdf = pd.DataFrame(list(cursor))
        self.bond_value = 6.99 / ((
            dirty_df["13190"]['high'] +
            dirty_df["13190"]['low']) / 2)
        self.ha_price = round((
            dirty_df["561"]['high'] +
            dirty_df["561"]['low']) / 2, 0)
        
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
                high_alch.append(self.cdf['highalch'][i] - item_price[i] - self.ha_price)
            except:
                item_price.append(0)
                true_value.append(0)
                high_alch.append(self.cdf['highalch'][i] - item_price[i] - self.ha_price)
        
        self.cdf["ge_price"] = item_price
        self.cdf['usd_value'] = true_value
        self.cdf['ha_profit'] = high_alch
        # Dropping the _id column that was created when sending into the DB.
        self.cdf.drop(columns="_id", inplace=True)
        
    @staticmethod
    def autoplay_audio(file_path: str):
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