from pymongo import MongoClient
from assign import settings

class Process:
    def __init__(self):
        client = MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )

        db = client[settings.MONGODB_DB]
        for collection in settings.MONGODB_COLLECTION:
            if collection not in db.collection_names():
                collection = db.create_collection(collection)
        self.blog_collection = db[settings.MONGODB_COLLECTION[0]]
        self.meta_collection = db[settings.MONGODB_COLLECTION[1]]

    def process(self, item):
        col = {
            'url': item['url'],
            'heading': item['header']
        }
        self.blog_collection.insert(dict(col))

        # save meta data of the blog in table 2 - 'meta'
        col2 = {
            'url': item['url'],
            'description': item['desc'],
            'image': item['image'],
            'title': item['title'],
            'vote': item['vote']
        }
        self.meta_collection.insert(dict(col2))
        return item
