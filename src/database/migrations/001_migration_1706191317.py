from contextlib import suppress
import peewee as pw
from peewee_migrate import Migrator
from services.users.models.user import User

with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.add_fields(User, status=pw.CharField(null=True))
    
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    pass
    
