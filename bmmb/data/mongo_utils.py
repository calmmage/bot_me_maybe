# mongoengine utils
from typing import Type

import mongoengine
from pymongo.collection import Collection
from pymongo.database import Database


def get_conn_str():
    from dotenv import load_dotenv
    load_dotenv()
    import os
    conn_str = os.getenv("MONGO_CONNECTION_STRING")
    assert conn_str
    return conn_str


def connect_mongo(alias):
    conn_str = get_conn_str()
    # 1.2: connect, using connection string, db_name=app and alias=app
    return mongoengine.connect(db=alias, alias=alias, host=conn_str)


class MongoItem(mongoengine.Document):

    def __repr__(self):
        fields = {}
        for field in self._fields_ordered:
            if field in ['id', '_id', '_cls']:
                continue
            fields[field] = getattr(self, field)
        field_values = ', '.join(f"{key}: {val}" for key, val in fields.items())
        return f"<{self.__class__.__name__}({field_values})>"

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.objects)

    meta = {"abstract": True, "strict": False, "allow_inheritance": True}


class MongoTable:
    def __init__(self, table_name, item_type, db_alias=None):
        self.table_name = table_name
        self.item_type = item_type
        if db_alias is not None:
            self.db_alias = db_alias

    @property
    def db_alias(self):
        return self.item_type._meta.get('db_alias')

    @db_alias.setter
    def db_alias(self, value):
        if 'db_alias' in self.item_type._meta:
            if self.item_type._meta['db_alias'] != value:
                raise ValueError(
                    f"db_alias {value} does not match "
                    f"item_type._meta['db_alias'] "
                    f"{self.item_type._meta['db_alias']}")
        self.item_type._meta['db_alias'] = value

    def get_all_items(self):
        items = self.item_type.objects.all()
        return items

    def get_item(self, **kwargs):
        item = self.item_type.objects(**kwargs).first()
        return item

    def get_item_by_id(self, item_id):
        item = self.item_type.objects(id=item_id).first()
        return item

    def insert_item(self, item):
        if isinstance(item, dict):
            item = self.item_type(**item)
        item.save()

    def add_item(self, **item_data):
        item = self.item_type(**item_data)
        item.save()

    def update_item(self, item_id, item_data):
        item = self.item_type.objects(id=item_id).first()
        for key, value in item_data.items():
            setattr(item, key, value)
        item.save()

    def delete_item(self, item_id):
        item = self.item_type.objects(id=item_id).first()
        item.delete()

    PREVIEW_HEAD = 3
    PREVIEW_TAIL = 3

    def __repr__(self):
        total_items_count = self.item_type.objects.count()

        items = self.item_type.objects.order_by('id')
        head_items = items.limit(self.PREVIEW_HEAD)

        reverse_items = self.item_type.objects.order_by('-id')
        tail_items = reverse_items.limit(self.PREVIEW_TAIL)

        preview_strings = ([f"  {repr(item)}" for item in head_items] +
                           ['  ...'] +
                           [f"  {repr(item)}" for item in reversed(tail_items)])
        preview_output = '\n'.join(preview_strings)
        return f"<{self.__class__.__name__} for '{self.table_name}': {total_items_count} items>\n{preview_output}"

    def as_dataframe(self):
        import pandas as pd
        items = self.get_all_items()
        df = pd.DataFrame(items)
        return df

    as_df = as_dataframe

    def __getattr__(self, item):
        return getattr(self.item_type, item)

    def __getitem__(self, item):
        return self.item_type[item]


# import mongoengine
# from dotenv import load_dotenv
# load_dotenv()
# import os
# conn_str = os.getenv("MONGO_CONNECTION_STRING")
from mongoengine.connection import ConnectionFailure


class MongoDatabase:
    def __init__(self, db_name, db_alias='default', conn_str=None):
        self.db_name = db_name
        self.db_alias = db_alias
        # if already connected - reuse
        try:
            self.db: Database = mongoengine.connection.get_db(db_alias)
            if conn_str is not None:
                original_conn_str = \
                    self.db.client._MongoClient__init_kwargs['host'][0]
                assert original_conn_str == conn_str
        except ConnectionFailure:
            client = mongoengine.connect(host=conn_str, db=db_name,
                                         alias=db_alias)
            self.db: Database = client.get_database(db_alias)

        # option 1: load all tables from db to memory
        # option 2: check if table exists in db when needed
        self.tables = {}

    def list_tables(self):
        return list(self.tables.keys())

    def list_collections(self):
        return self.db.list_collection_names()

    def get_collection_fields(self, collection_name, mode='last'):
        collection = self.get_collection(collection_name)
        if mode == 'first':
            item = collection.find_one()
            return list(item.keys())
        elif mode == 'last':
            item = collection.find().sort('_id', -1).limit(1).next()
            return list(item.keys())
        elif mode == 'all':
            # Define the aggregation pipeline
            pipeline = [
                {'$project': {'_id': 0,
                              'fields': {'$objectToArray': '$$ROOT'}}},
                {'$unwind': '$fields'},
                {'$group': {'_id': '$fields.k', 'count': {'$sum': 1}}}
            ]
            # Execute the aggregation pipeline and print the results
            result = collection.aggregate(pipeline)
            return {doc['_id']: doc['count'] for doc in result}

    def get_table(self, table_name) -> MongoTable:
        return self.tables[table_name]

    def get_collection(self, table_name) -> Collection:
        return self.db[table_name]

    def create_table(
            self,
            table_name: str,
            item_type: Type[mongoengine.Document]
    ) -> MongoTable:
        # check if table exists
        if table_name in self.tables:
            raise ValueError(f"Table {table_name} already exists")
        # create table
        table = MongoTable(table_name, item_type, db_alias=self.db_alias)
        # save table info to db
        self.tables[table_name] = table
        return table

    def add_table(self, table: MongoTable) -> MongoTable:
        # check if table exists
        if table.table_name in self.tables:
            raise ValueError(f"Table {table.table_name} already exists")
        # check if table meta points to this db
        if table.db_alias is not None:
            if table.db_alias != self.db_alias:
                raise ValueError(
                    f"Table {table.table_name} is not connected to this db")
        else:
            table.db_alias = self.db_alias
        # save table info to db
        self.tables[table.table_name] = table
        return table

    connect_table = add_table

    def has_table(self, table_name):
        return table_name in self.tables

    def has_collection(self, collection_name):
        return collection_name in self.db.list_collection_names()

    def __getitem__(self, item):
        if self.has_table(item):
            return self.get_table(item)
        elif self.has_collection(item):
            return self.get_collection(item)
        else:
            raise KeyError(f"Table {item} does not exist")

    def __getattr__(self, key):
        return getattr(self.db, key)
