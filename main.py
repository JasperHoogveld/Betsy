from operator import contains
from models import *

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


def search(term) -> list:
    products = []
    term = term.lower()
    query = (Product.select()
            .where(fn.LOWER(Product.name).contains(term) or fn.LOWER(Product.description).contains(term)))
    products = [prod for prod in query]
    if not products:
        print(f'{term} was not found!')
    return products


def list_user_products(user) -> list:
    if user is None:
        return f'User was not found!'
    user_products = []
    query = (Product.select()
            .where(Product.owner == user))
    user_products = [prod for prod in query]
    if not user_products:
        print(f'No products found for {user.name}')
    return user_products
    

def list_products_per_tag(tag) -> list:
    tag_products = []
    query = (Product.select()
             .join(Tags, on=(Product.id == Tags.id))
             .where(fn.LOWER(Product.name).contains(fn.LOWER(tag))))
    tag_products = [prod.name for prod in query]
    if not tag_products:
        print(f'No products with the name {tag} found')
    return tag_products


def add_product_to_catalog(user_id, product) -> str:
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        return f'That user is not valid'
    product.owner = user
    product.save()
    return f'Product with {product.name} added to catalog of {user.name}'


def update_stock(product_id, new_quantity) -> str:
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        return f'That product ID is not valid'
    product.qty_in_stock = new_quantity
    product.save()
    return f'Product with ID {product_id} has now {new_quantity} in stock'


def purchase_product(product_id, buyer_id, quantity) -> str:
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        return f'Product does not exist'
    if quantity > product.qty_in_stock:
        return f'Not enough in stock'
    try:
        buyer = User.get_by_id(buyer_id)
    except DoesNotExist:
        return f'User does not exist'
    product.qty_in_stock -= quantity
    product.save()
    transaction = Transaction()
    transaction.product = product
    transaction.buyer = buyer
    transaction.price_per_unit = product.price_per_unit
    transaction.qty_sold = quantity
    transaction.save()
    tot_price = transaction.price_per_unit * transaction.qty_sold
    return f'{quantity} of {product.name} sold to {buyer.name} for {tot_price}'


def remove_product(product_id) -> str:
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        return 'That product ID is not valid'
    product.delete()
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


populate_test_database()

user1 = User.select().where(User.name == 'Jasper').first()
user3 = User.select().where(User.name == 'Koos').first()
tag1 = 'fRidge'
prod1 = Product.select().where(Product.name == 'small_white_fridge').first()
prod2 = Product.select().where(Product.name == 'large_black_fridge').first()
prod3 = Product(name='small_black_fridge', description='small black fridge', price_per_unit=11, qty_in_stock=3)

print(search('fridgsde'))
# print(list_user_products(user3))
# print(list_products_per_tag(tag1))
# print(add_product_to_catalog(1, prod3))
# print(update_stock(prod1.id, 2))
# print(purchase_product(prod2.id, user1.id, 1))
# print(purchase_product(None, user1.id, 1))
# print(purchase_product(prod2.id, 12, 1))
# print(purchase_product(prod2.id, user1.id, 3456))
# print(remove_product(prod1.id))
# print(remove_product(5))