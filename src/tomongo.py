from base import Base
import pymongo
import os

class ToMongo(Base):
    def __init__(self):
        # Load the env variables:
        # self.__mongo_url = os.getenv("MONGO_URL")
        #Connect to PyMongo
        self.client = pymongo.MongoClient(
            """mongodb+srv://prophetseven:FLo9JtqJx3EStYEP@cluster0.xnkg2ge.mongodb.net/?retryWrites=true&w=majority"""
            )
        # Create a database
        self.db = self.client.db
        # Create a collection:
        self.runescape_items = self.db.runescape_items

    def upload_one_by_one(self):
        self.runescape_items.drop()
        Base.__init__(self)
        for i in self.df.index:
            self.runescape_items.insert_one(self.df.loc[i].to_dict())
            

if __name__ == '__main__':
    c = ToMongo()
    print('Successful Connection to Client Object')
    c.upload_one_by_one()
    print('Successfully Uploaded all Park Info to Mongo')