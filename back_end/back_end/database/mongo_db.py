from pymongo import MongoClient
import gridfs
from urllib import parse
from bson import ObjectId


class MongoDB:
    def __init__(self):
        self.db = None

    def init_app(self, app):
        mongo_url = f'mongodb://{parse.quote_plus(app.config["MONGO_USER"])}:{parse.quote_plus(app.config["MONGO_PASSWORD"])}@{app.config["MONGO_HOST"]}:{app.config["MONGO_PORT"]}'
        client = MongoClient(mongo_url)
        self.db = client[app.config['MONGO_DB']]
    def get_file(self, file_id: str) -> bytes:
        fs = gridfs.GridFS(self.db, 'file')
        gf = fs.get(ObjectId(file_id))
        return gf.read()

    def save_file(self, file) -> str:
        fs = gridfs.GridFS(self.db, 'file')
        file_id = str(fs.put(file))
        return file_id

    def delete_file(self, file_id: str):
        fs = gridfs.GridFS(self.db, 'file')
        fs.delete(ObjectId(file_id))
