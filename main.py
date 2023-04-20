from operator import contains
from models import *
from peewee import DoesNotExist

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"
 

def search(term):
    while True:

        try:    
            products = []
            term = term.lower()
            query = (Product.select()
                    .where(fn.LOWER(Product.name).contains(term.lower()) or fn.LOWER(Product.description).contains(term.lower())))
            products = [prod for prod in query]
            if not products:
                return print(f'{term} was not found!') 
            else:
                return products
        except ValueError:
            print('No term supplied')

    
    


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
             .where(fn.LOWER(Product.name).contains(fn.LOWER(tag))))
    tag_products = [prod for prod in query]
    return tag_products


def add_product_to_catalog(user_id, product):
    # query = (User.select()
    #          .where(User.id == user_id))
    # new_prod = query.insert(product)
    # new_prod.execute()
    # new_prod = new_prod.update(new_prod.owner == user_id)
    query = (Product.create(product))
    # query.update(query.owner == user_id)
    # query.execute()
    return print(f'Product with {product.name} added to catalog')


def update_stock(product_id, new_quantity):
    ...


def purchase_product(product_id, buyer_id, quantity):
    query = (Product.update()
             .join(User, on=(Product.owner == User.id))
             .where(Product.id == product_id and User.id == buyer_id))
    ## Nope


def remove_product(product_id):
    query = (Product.delete()
             .where(Product.id == product_id))
    query.execute()

    return print(f'Product with ID {product_id} removed')

def populate_test_database():
    #Tags
    fridge = Tags(name = 'fridge')
    small = Tags(name = 'small')
    large = Tags(name = 'large')
    white = Tags(name = 'white')
    black = Tags(name = 'black')
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

    # small_black_fridge = Product(name='small_black_fridge', description='small black fridge', price_per_unit=11, qty_in_stock=3)
    # small_black_fridge.save()
    # small_black_fridge.tags = [small, black, fridge]
    # small_black_fridge.save()

    # small_black_fridge = Product(name='small_black_fridge', description='small black fridge', price_per_unit=11, qty_in_stock=5, tags=['small', 'black', 'fridge'])
    # small_black_fridge.save()
    # large_white_fridge = Product(name='large_white_fridge', description='large white fridge', price_per_unit=18, qty_in_stock=5, tags=['large', 'white', 'fridge'])
    # large_white_fridge.save()
    # large_black_fridge = Product(name='large_black_fridge', description='large black fridge', price_per_unit=19, qty_in_stock=5, tags=['large', 'black', 'fridge'])
    # large_black_fridge.save()




populate_test_database()

user1 = User.select().where(User.name == 'Jasper').first()
tag1 = 'fRidge'
prod1 = Product(name='small_black_fridge', description='small black fridge', price_per_unit=11, qty_in_stock=3)
prod2 = Product.select().where(Product.name == 'large_black_fridge').first()
print(search())
#print(list_user_products(user1))
#print(list_products_per_tag(tag1))
#print(add_product_to_catalog(user1.id, prod1))
#print(update_stock(prod1.id, 2))
#print(purchase_product(prod2.id, user1.id, 1))
#print(remove_product(prod1.id))