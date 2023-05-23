from peewee import *
import os
import sys

# dbase = os.path.join(sys.path[0], 'betsy_webshop.db')
# db = peewee.SqliteDatabase(dbase)
db = SqliteDatabase(":memory:")

class BaseModel(Model):
    class Meta:
        database = db

class Tags(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True, null=False)

class User(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True, null=False)
    address = CharField(null=False)
    billing = CharField(null=False)

class Product(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(null=False)
    description = CharField()
    price_per_unit = DecimalField(decimal_places=2, auto_round=True, constraints=[Check('price_per_unit > 0')])
    qty_in_stock = IntegerField(null=False)
    tags = ManyToManyField(Tags, backref="products")
    owner = ForeignKeyField(User, backref="products", null=True)

class Transaction(BaseModel):
    id = IntegerField(primary_key=True)
    product = ForeignKeyField(Product, backref="transactions")
    buyer = ForeignKeyField(User)
    price_per_unit = IntegerField()
    qty_sold = IntegerField()

ProductTags = Product.tags.get_through_model()


db.connect()
db.create_tables([Tags, Product, User, Transaction, ProductTags])

