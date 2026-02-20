from pymongo import MongoClient
from flask import current_app, g

mongo_client = None
db = None


def init_db(app):
    global mongo_client, db
    
    mongo_uri = app.config['MONGO_URI']
    mongo_client = MongoClient(mongo_uri)
    
    # Extract database name from URI or use default
    db_name = mongo_uri.split('/')[-1].split('?')[0]
    if not db_name or db_name.startswith('mongodb'):
        db_name = 'workout_db'
    
    db = mongo_client[db_name]
    
    app.teardown_appcontext(close_db)


def get_db():
    if 'db' not in g:
        if db is None:
            raise RuntimeError(
                "Database not initialized. Make sure init_db() is called during app setup."
            )
        g.db = db
    return g.db


def close_db(e=None):
    db = g.pop('db', None)