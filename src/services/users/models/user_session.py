from playhouse.postgres_ext import (
    UUIDField,
    SQL,
    CharField,
    DateTimeField,
    TextField,
)
from datetime import datetime
from database.base_model import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSession(BaseModel):
  id = UUIDField(constraints=[SQL("DEFAULT gen_random_uuid()")], primary_key=True)
  user_id = UUIDField()
  status = CharField()
  auth_mode = CharField()
  token = TextField()
  expire_at = DateTimeField(null=True)
  password_digest = CharField(null=True)
  created_at = DateTimeField(default=datetime.utcnow)
  updated_at = DateTimeField(default=datetime.utcnow, index=True)

  class Meta:
    table_name = "user_sessions"

  def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(UserSession, self).save(*args, **kwargs)