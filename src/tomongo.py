from base import Base
import pymongo


class ToMongo(Base):
    """
    This object inherits from Base class. The main reason for this is to
    be able to initialize the base class to grab the clean data frame to then
    send to the Mongo DB. The main purpose of this object is to easily access
    the database's collection and also to upload the cleaned data frame to the
    Mongo DB

    The attributes of this class are:
        -Client: String; this is to connect to the database using pymongo.
        -db; DataBase; This is either create or connect to a data base
            named "db".
        -RuneScape Items: Collection; Creates or connects to the collection
            named "runescape_items".
    The method for this class is:
        -upload one by one: The first thing this does is drop the collection
            from the data base so as to not duplicate any item and also due to
            the possibility of changing integers from nerfs or buffs. Then, it
            initailizes the base class to query the data and clean it. It then
            uploads each row of data one by one into the collection to make\
            sure no data leakage happens.
    """
    def __init__(self):
        # Connect to PyMongo.
        # Due to the finickiness of Streamlit, I have to keep the string as
        #   a whole line just to get it to publish correctly.
        self.client = pymongo.MongoClient(
            """mongodb+srv://prophetseven:FLo9JtqJx3EStYEP@cluster0.xnkg2ge.mongodb.net/?retryWrites=true&w=majority"""
            )
        # Create a database
        self.db = self.client.db
        # Create a collection:
        self.runescape_items = self.db.runescape_items

    def upload_one_by_one(self):
        # Drops the original collection to not duplicate and so as to update
        # any changed information.
        self.runescape_items.drop()
        Base.__init__(self)
        for i in self.df.index:
            self.runescape_items.insert_one(self.df.loc[i].to_dict())
            

if __name__ == '__main__':
    c = ToMongo()
    print('Successful Connection to Client Object')
    c.upload_one_by_one()
    print('Successfully Uploaded all Park Info to Mongo')