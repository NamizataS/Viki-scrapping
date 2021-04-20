from pymongo import MongoClient
import pandas as pd


class Database:
    def __init__(self):
        self.client = MongoClient()
        self.db_viki = self.client.viki
        self.collection_viki = self.db_viki['shows']

    def insert(self, df):
        shows = df.fillna("").to_dict(orient='records')
        self.collection_viki.insert_many(shows)
        print('Insert done')

    def update(self, df):
        shows = df.fillna("").to_dict(orient='records')
        for document in shows:
            self.collection_viki.update_one({'Nom': document['Nom']}, {'$set': document}, upsert=True)
        print('Update done')

    def get_types(self):
        cur = self.collection_viki.aggregate([{"$group": {"_id": "$Type", "TypeShows": {"$sum": 1}}}])
        return cur

    def get_countries(self):
        cur = self.collection_viki.aggregate(
            [{"$group": {"_id": "$Pays", "showsNumber": {"$sum": 1}}}, {'$sort': {'showsNumber': -1}}])
        return cur

    def get_on_air(self):
        cur = self.collection_viki.aggregate(
            [{"$group": {"_id": "$on_air", "showsNumber": {"$sum": 1}}}, {"$sort": {"showsNumber": -1}}])
        return cur

    def get_best_tv_shows(self):
        cur_best_tv_shows = self.collection_viki.find({'Type': 'Série'}).sort('Note', -1).limit(5)
        return cur_best_tv_shows

    def get_countries_types(self):
        cur = self.collection_viki.aggregate(
            [{"$group": {"_id": {"pays": "$Pays", "type": "$Type"}, "showsNumber": {"$sum": 1}}},
             {'$sort': {'showsNumber': -1}}])
        return cur
