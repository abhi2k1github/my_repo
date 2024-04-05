from database.db_session import db
from services.users.models.user import User
from services.users.models.user_session import UserSession

def create_tables():
    try:
        db.create_tables([UserSession])
        db.close()
        print("created tables")
    except:
        print("Exception while creating table")
        raise
