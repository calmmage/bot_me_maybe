import logging
from bmmb.data.mongo_utils import MongoItem, MongoTable, connect_mongo
import mongoengine


class LogItem(MongoItem):
    timestamp = mongoengine.DateTimeField(required=True)
    level = mongoengine.StringField(required=True)
    message = mongoengine.StringField(required=True)
    extra = mongoengine.DictField()


class MongoHandler(logging.Handler):
    def __init__(self, mongo_table: MongoTable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_table = mongo_table

    def emit(self, record):
        try:
            extra = record.__dict__.pop('extra')
        except KeyError:
            extra = None

        self.mongo_table.insert_item(
            timestamp=record.created,
            level=record.levelname,
            message=record.getMessage(),
            extra=extra
        )
        log_item = LogItem(
            timestamp=record.created,
            level=record.levelname,
            message=record.getMessage(),
            extra=extra
        )
        log_item.save()
