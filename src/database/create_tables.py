from database.db_session import db
from services.users.models.user import User

def create_tables():
    try:
        db.create_tables([User])
        db.close()
        print("created tables")
    except:
        print("Exception while creating table")
        raise
