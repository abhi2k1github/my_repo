from playhouse.signals import Model
from database.db_session import db
from playhouse.shortcuts import ThreadSafeDatabaseMetadata


class BaseModel(Model):
    class Meta:
        database = db
        only_save_dirty = True
        model_metadata_class = ThreadSafeDatabaseMetadata
