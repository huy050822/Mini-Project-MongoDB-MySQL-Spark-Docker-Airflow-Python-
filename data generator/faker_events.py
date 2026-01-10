import json
import time
import uuid
import random
import logging
from datetime import timedelta, datetime
from faker import Faker
from config.logging_config import get_logger

logger = logging.getLogger("faker_events", "data")
fake = Faker()

class Procedure():
    #Init function
    def __init__(self,num_users,num_products,min_sleep,max_sleep):
        self.num_users = num_users
        self.num_products = num_products
        self.min_sleep = min_sleep
        self.max_sleep = max_sleep
        self.config = {
            "num_users" : num_users,
            "num_products" : num_products,
            "min_sleep" : min_sleep,
            "max_sleep" : max_sleep
        }
        self.users = None
        self.products = None
        self.categories = None
        self.stock = None
        self.warehouse = ["WH01", "WH02", "WH03"]
    #Repr function
    def __repr__(self):
        return f"Fake_events(num_users:{self.num_users}, num_products:{self.num_products})"
    
    #Create categories
    def create_categories(self):
        self.categories = [{"category_id": 1, "category_name": "food"}, 
        {"category_id": 2, "category_name": "drink"}, 
        {"category_id": 3, "category_name": "electronics"},
        {"category_id": 4, "category_name": "clothes"} 
        ]
        return self.categories
    
    #Create user
    def create_user(self):
        self.users = []

        for i in range(1, self.num_users + 1):
            user_id = i
            user_name = fake.name()
            user_address = fake.address()
            user_country = fake.country()
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            user = {
                "user_id": user_id,
                "user_name": user_name,
                "user_address": user_address,
                "user_country": user_country,
                "created_at" : created_at
            }
            self.users.append(user)
    
    #Create product
    def create_products(self):
        if not self.categories:
            return self.create_categories()
        self.products = []
        for i in range(1, self.num_products + 1):
            choice = random.choice(self.categories)
            product_id = i
            product_name = f"Product {i}"
            price = round(random.uniform(1,500))
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            product = {
                "product_id" : product_id,
                "product_name" : product_name,
                "categories_id" : choice[choice],
                "price" : price,
                "created_at" : created_at
            }
            self.products.append(product)

    #Create stock => If product is not exist => stock raise 
    def create_stock(self, min_quantity = 20, max_quantity = 300):
        self.stock = []
        for product in self.products:
            product_id = product["product_id"] 
            warehouse_id = random.choice(self.warehouse)
            quantity_served = random.randint(min_quantity, max_quantity)
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            stock = {
                "product_id" : product_id,
                "warehouse_id" : warehouse_id,
                "quantity_served": quantity_served,
                "quantity_reserved" : 0,
                "created_at" : created_at
            }
        
        self.stock.append(stock)
        
