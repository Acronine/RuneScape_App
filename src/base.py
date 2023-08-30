import pandas as pd
import requests, json
from string import ascii_lowercase
import numpy as np

class Base:
    
    api_url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
    def __init__(self):
        self.header = {
            'User-Agent': 'My User Agent 1.0',
            'From': "@TheFirmPenguin#8408"
            }
        self.wrangle()
    
    def wrangle(self):
        df = requests.get(fr"{self.api_url}",headers=self.header)
        item_list = {}
        for itemz in df.json():
            item = self.item_setup(itemz)
            item_list[(item['name'])] = item
        correct_df = pd.DataFrame.from_dict(item_list)
        self.df = correct_df.transpose().reset_index()
        self.df.drop('index',axis=1,inplace=True) 
        
    @staticmethod
    def item_setup(item:dict):
        image_url = (
            f"""https://oldschool.runescape.wiki/images/{
                (item['icon']).replace(' ','_')
                }"""
            )
        # Checking 'members' boolean to set matching membership icon url.
        # Also, VStudio is telling me the (==) needs to be (is),
        #   but it breaks the app when set to that.
        if item['members'] == True:
            members_url = (r'https://oldschool.runescape.wiki/images/Member_icon.png')
        elif item['members'] == False:
            members_url = (r'https://oldschool.runescape.wiki/images/Free-to-play_icon.png')
        
        item_info = {'name': item['name'],
            'icon': image_url,
            'id':item['id'],
            'description':item['examine'],
            "members": members_url,
            "gp_value": item['value'],

            }
        for key in ["lowalch", "limit", "highalch"]:
            if key not in item.keys():
                item_info[key] = 0
            else:
                item_info[key] = item[key]
        return item_info
    
if __name__== '__main__':
    c=Base()
    c.df.to_csv('src/data/runescape_info.csv', index=False)