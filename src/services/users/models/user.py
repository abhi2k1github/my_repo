from playhouse.postgres_ext import (
    UUIDField,
    SQL,
    CharField,
    DateTimeField,
)
from datetime import datetime
from database.base_model import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
  id = UUIDField(constraints=[SQL("DEFAULT gen_random_uuid()")], primary_key=True)
  name = CharField()
  email = CharField()
  mobile_number = CharField()
  mobile_country_code = CharField()
  password_digest = CharField(null=True)
  status = CharField(null=True)
  created_at = DateTimeField(default=datetime.utcnow)
  updated_at = DateTimeField(default=datetime.utcnow, index=True)

  class Meta:
    table_name = "users"

  def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(User, self).save(*args, **kwargs)

  def verify_password(self, plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

  def get_password_hash(self, password):
      return pwd_context.hash(password)
