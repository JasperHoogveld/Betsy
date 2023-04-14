from operator import contains
from models import *

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"
 

def search(term):
    products = []
    if not term:
        print('No term supplied')
    term = term.lower()
    query = (Product.select()
             .where(fn.LOWER(Product.name).contains(term.lower()) or fn.LOWER(Product.description).contains(term.lower())))
    products = [prod for prod in query]
    return products


def list_user_products(user):
    user_products = []
    query = (Product.select()
             .where(Product.owner == user))
    user_products = [prod for prod in query]
    return user_products


def list_products_per_tag(tag):
    tag_products = []
    query = (Product.select()
             .join(Tags, on=(Product.id == Tags.id))
             .where(Tags.name == tag))
    tag_products = [prod for prod in query]
    return tag_products


def add_product_to_catalog(user_id, product):
    query = (User.select()
             .join(Product())
             .where(User.id == user_id)
            )
    query.insert(product) # NOPE
    query = (User.select()
             .join(Product())
             .where(User.id == user_id)
            )
    new_prod_list = [prod for prod in query]
    return print(new_prod_list)    


def update_stock(product_id, new_quantity):
    ...


def purchase_product(product_id, buyer_id, quantity):
    ...


def remove_product(product_id):
    ...

def populate_test_database():
    #Tags
    small = Tags(name = 'small')
    large = Tags(name = 'large')
    white = Tags(name = 'white')
    black = Tags(name = 'black')
    fridge = Tags(name = 'fridge')
    small.save()
    large.save()
    white.save()
    black.save()
    fridge.save()

    # Users
    jasper = User(name='Jasper', address='street 5, 1234ab, amsterdam', billing='street 5, 1234ab, amsterdam')
    piet = User(name='Piet', address='lane 8, 1234cd, kudel', billing='lane 8, 1234cd, kudel')
    jasper.save()
    piet.save()

    # Products
    small_white_fridge = Product(name='small_white_fridge', description='small white fridge', price_per_unit=10, qty_in_stock=5, owner=jasper)
    small_white_fridge.save()
    small_white_fridge.tags = [small, white, fridge]
    small_white_fridge.save()

    large_black_fridge = Product(name='large_black_fridge', description='large black fridge', price_per_unit=19, qty_in_stock=3, owner=piet)
    large_black_fridge.save()
    large_black_fridge.tags = [large, black, fridge]
    large_black_fridge.save()

    small_black_fridge = Product(name='small_black_fridge', description='small black fridge', price_per_unit=11, qty_in_stock=3)
    small_black_fridge.save()
    small_black_fridge.tags = [small, black, fridge]
    small_black_fridge.save()

    # small_black_fridge = Product(name='small_black_fridge', description='small black fridge', price_per_unit=11, qty_in_stock=5, tags=['small', 'black', 'fridge'])
    # small_black_fridge.save()
    # large_white_fridge = Product(name='large_white_fridge', description='large white fridge', price_per_unit=18, qty_in_stock=5, tags=['large', 'white', 'fridge'])
    # large_white_fridge.save()
    # large_black_fridge = Product(name='large_black_fridge', description='large black fridge', price_per_unit=19, qty_in_stock=5, tags=['large', 'black', 'fridge'])
    # large_black_fridge.save()




populate_test_database()

user1 = User.select().where(User.name == 'Jasper').first()
tag1 = Tags.select().where(Tags.name == 'fridge').first()
prod1 = Product.select().where(Product.name == 'small_black_fridge').first()
#print(search('Fridge'))
#print(list_user_products(user1))
#print(list_products_per_tag(tag1))
print(add_product_to_catalog(user1, prod1))