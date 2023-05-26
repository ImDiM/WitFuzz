import os.path
from urllib import parse
from pymongo import MongoClient
import gridfs
from bson import ObjectId


class MongoDB:
    def __init__(self, config):
        mongo_url = f'mongodb://{parse.quote_plus(config["app"]["MONGO_USER"])}:{parse.quote_plus(config["app"]["MONGO_PASSWORD"])}@{config["app"]["MONGO_HOST"]}:{config["app"]["MONGO_PORT"]}'
        client = MongoClient(mongo_url)
        self.db = client[config['app']['MONGO_DB']]

    def get_file(self, file_id: str, file_name: str, file_dir: str):
        '''
        get file from mongodb and save to local dir
        :param file_id:
        :param file_name:
        :param file_dir:
        :return:
        '''
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        fs = gridfs.GridFS(self.db, 'file')
        gf = fs.get(ObjectId(file_id))
        with open(os.path.join(file_dir, file_name), 'wb') as f:
            f.write(gf.read())

    def save_file(self, file_name: str, file_dir: str) -> str:
        '''
        save file to mongodb
        :param file_name:
        :param file_dir:
        :return:
        '''
        fs = gridfs.GridFS(self.db, 'file')
        with open(os.path.join(file_dir, file_name), 'rb') as f:
            return fs.put(f.read())
