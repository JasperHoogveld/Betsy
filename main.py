from operator import contains
from models import *

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


def search(term):
    products = []
    term = term.lower()
    query = (Product.select()
            .where(fn.LOWER(Product.name).contains(term.lower()) or fn.LOWER(Product.description).contains(term.lower())))
    products = [prod for prod in query]
    if not products:
        print(f'{term} was not found!')
    return products


def list_user_products(user):
    if user is None:
        return print(f'User was not found!')
    user_products = []
    query = (Product.select()
            .where(Product.owner == user))
    user_products = [prod for prod in query]
    if user_products:
        return print(user_products)
    return print(f'No products found for {user.name}')


def list_products_per_tag(tag):
    tag_products = []
    query = (Product.select()
             .join(Tags, on=(Product.id == Tags.id))
             .where(fn.LOWER(Product.name).contains(fn.LOWER(tag))))
    tag_products = [prod for prod in query]
    if tag_products:
        return print(tag_products)
    return print(f'No products with the name {tag} found')


def add_product_to_catalog(user_id: int, product: Product):
    user = (User.select()
            .where(User.id == user_id).first())
    if user:
        product.owner = user
        product.save()
        print(f'Product with {product.name} added to catalog of {user.name}')
        return True
    else:
        print(f'{user_id} does not exist')
        return False


def update_stock(product_id, new_quantity):
    if product_id is None or (Product.select().where(Product.id == product_id).first()) is None:
        return 'That product ID is not valid'
    query = (Product.update(qty_in_stock = new_quantity)
             .where(Product.id == product_id))
    query.execute()
    return f'Product with ID {product_id} has now {new_quantity} in stock'

def purchase_product(product_id, buyer_id, quantity):
    if product_id is None or (Product.select().where(Product.id == product_id).first()) is None:
        return 'That product ID is not valid'
    elif quantity > (Product.select(Product.qty_in_stock).where(Product.id == product_id).first()):
        return f'Not enough in stock'
    else:
        new_qty_in_stock = (Product.select(Product.qty_in_stock).where(Product.id == product_id).first()) - quantity
        query = (Product.update(qty_in_stock = new_qty_in_stock)
             .where(Product.id == product_id))
        query.execute()
        buy_query = (Product.select()
                     .where(Product.owner == buyer_id))
        buy_query = (Product.update(qty_in_stock =+ quantity)
             .where(Product.id == product_id))   
        buy_query.execute()     
        return f'{quantity} of product with ID {product_id} sold to buyer with ID {buyer_id}'
    


def remove_product(product_id):
    if product_id is None or (Product.select().where(Product.id == product_id).first()) is None:
        return 'That product ID is not valid'
    query = (Product.delete()
             .where(Product.id == product_id))
    query.execute()
    return f'Product with ID {product_id} removed'


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
    koos = User(name='Koos', address='lane 9, 1234cd, kudel', billing='lane 9, 1234cd, kudel')
    jasper.save()
    piet.save()
    koos.save()

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
user3 = User.select().where(User.name == 'Koos').first()
tag1 = 'fRidge'
prod1 = Product.select().where(Product.name == 'small_white_fridge').first()
prod2 = Product.select().where(Product.name == 'large_black_fridge').first()
prod3 = Product(name='small_black_fridge', description='small black fridge', price_per_unit=11, qty_in_stock=3)
#search('fridgsde')
#list_user_products(user3)
#list_products_per_tag(tag1)
#add_product_to_catalog(1, prod3)
#print(update_stock(prod1.id, 2))
print(purchase_product(prod2.id, user1.id, 1))
#print(remove_product(prod1.id))
#remove_product(5)