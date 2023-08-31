import pandas as pd
import requests, json


# Creating the Base Class
class Base:
    """
    The purpose of this object is to query from the RuneScape Wiki's Map Api
    and to clean and tidy the data.

    The attributes for this class are:
        -Api Url: String; This is the url for the mapping data of all items
        that can be traded on the Grand Exchange.
        -Header: Dictionary; The api requires a user agent to gain access
            to their content.
        -DF: DataFrame; This is the cleaned DataFrame that will be used to send
            to my Mongo DataBase.
    The methods for thi class are:
        -Wrangle: Queries the data from the RuneScape Wiki Api and cleans it.
        -Item Setup: A static method that each item is iterated through during
            wrangle to produce the desired structure for a data frame.
    """
    api_url = "https://prices.runescape.wiki/api/v1/osrs/mapping"

    def __init__(self):
        """
        Initiation of the base class. Sets the header attribute and calls to
        the wrangle function.
        """
        self.header = {
            'User-Agent': 'Pulling Mapping data to save to personal MongoDB',
            'From': "@TheFirmPenguin#8408"
            }
        self.wrangle()

    def wrangle(self):
        """
        Single Queries the data and cleans it into a data frame. Sets the
        cleaned dataframe as an attribute afterwards.
        """
        # Requests the data from the api.
        df = requests.get(fr"{self.api_url}", headers=self.header)
        # Creating an empty dictionary and filling with key:value pairs by
        # setting each item's name as the key.
        item_list = {}
        for itemz in df.json():
            item = self.item_setup(itemz)
            item_list[(item['name'])] = item
        # Creating a dataframe using that dictionary.
        correct_df = pd.DataFrame.from_dict(item_list)
        # Inverting the rows & columns and deleting the index to correct the
        #   structure of the dataframe while also setting to the df attribute.
        self.df = correct_df.transpose().reset_index()
        self.df.drop('index', axis=1, inplace=True) 

    @staticmethod
    def item_setup(item: dict):
        """
        The main method used to clean each item from the json file.
        """
        # The icon column is using the files as if they're inside the wiki's
        #   server. This is to correct the url to be able to be used.
        image_url = (
            f"""https://oldschool.runescape.wiki/images/{
                (item['icon']).replace(' ','_')
                }"""
            )
        # Checking 'members' boolean to set matching membership icon url.
        # Also, VStudio is telling me the (==) needs to be (is),
        #   but it breaks the app when set to that.
        if item['members'] == True:
            members_url = (
                r'https://oldschool.runescape.wiki/images/Member_icon.png'
                )
        elif item['members'] == False:
            members_url = (
                r'https://oldschool.runescape.wiki/images/Free-to-play_icon.png'
            )
        # Pulling each key from the item's dictionary and renaming the columns
        #   for better readability.
        item_info = {'name': item['name'],
                     'icon': image_url,
                     'id': item['id'],
                     'description': item['examine'],
                     "members": members_url,
                     "gp_value": item['value']
                     }
        # In the absence of any of these values, they are set to 0.
        for key in ["lowalch", "limit", "highalch"]:
            if key not in item.keys():
                item_info[key] = 0
            else:
                item_info[key] = item[key]

        return item_info


if __name__ == '__main__':
    c = Base()
    c.df.to_csv('src/data/runescape_info.csv', index=False)