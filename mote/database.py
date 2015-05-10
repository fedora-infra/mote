from peewee import *
import datetime
import config

# Connect to database using credentials from config.py
if config.dbtype == "mysql":
    db = MySQLDatabase(host=config.dbhost, user=config.dbuser, password=config.dbpass, database=config.dbname)
# Create models
class BaseModel(Model):
    class Meta:
        database = db

class PathAttr(BaseModel):
    added_by = CharField()
    # Regex Path Expression
    expression = CharField()
    # Friendly Name
    friendly_name = CharField()
    updated = DateTimeField(default=datetime.datetime.now)
