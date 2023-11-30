import logging
from conexion.mongo_queries import MongoQueries
import json

LIST_OF_COLLECTIONS = ["peruas", "motoristas", "responsaveis", "escolas", "alunos"]
logger = logging.getLogger(name="SGTE_CRUD_MONGODB")
logger.setLevel(level=logging.WARNING)
mongo = MongoQueries()

def createCollections(drop_if_exists:bool=False):

    mongo.connect()
    existing_collections = mongo.db.list_collection_names()
    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} droped!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} created!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} created!")
    mongo.close()

if __name__ == "__main__":
    logging.warning("Starting")
    createCollections(drop_if_exists=True)
    logging.warning("End")
