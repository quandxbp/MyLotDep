from common.credentials import MONGO_CRE

from pymongo import MongoClient


def mongo_connect():
    try:
        MONGO_URI = "mongodb://{USER}:{PASSWORD}@ds333248.mlab.com:{PORT}/{AUTH_SOURCE}?retryWrites=false"\
            .format(USER=MONGO_CRE['USER'],
                    PASSWORD=MONGO_CRE['PASSWORD'],
                    PORT=MONGO_CRE['PORT'],
                    AUTH_SOURCE=MONGO_CRE['AUTH_SOURCE'])
        client = MongoClient(MONGO_URI, connectTimeoutMS=30000)
        connection = client.get_database(MONGO_CRE['DB_NAME'])
        print("Mongo Database is connected")
        return connection
    except Exception as err:
        print("Error when connecting with Mongo Database")
        print(err)


class MongoDB:
    _connection = False
    _collection = False

    def __init__(self, collection):
        self._connection = mongo_connect()
        self._collection = self._connection[collection]

    def create_collection(self, collection_name):
        if collection_name not in self._connection.list_collection_names():
            new_col = self._connection[collection_name]
            if new_col:
                print("Successfully created Collection: %s" % collection_name)
        else:
            print("%s is already existed !" % collection_name)
        return True

    def insert_one(self, data):
        # Return an id of new record
        collection = self._collection
        new_record = collection.insert_one(data)
        return new_record

    def insert_many(self, data_list):
        # Return ids new records
        if not isinstance(data_list, list):
            print("data must list of new data")
        collection = self._collection
        new_records = collection.insert_many(data_list)
        return new_records.inserted_ids

    def find_one(self, search_fields, filter_list=[]):
        filter_fields = {x: 1 for x in filter_list}
        collection = self._collection
        data = collection.find_one(search_fields, filter_fields)
        return data

    def find_all(self, filter_fields={}):
        collection = self._collection
        data = collection.find({}, filter_fields)
        return data



