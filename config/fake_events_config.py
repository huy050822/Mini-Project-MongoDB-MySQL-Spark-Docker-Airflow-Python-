import os 
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class Fake_Events():
    num_users : int
    num_products : int
    min_sleep : float
    max_sleep : float

# def set_up_events():
#     load_dotenv()

#     config = { "fake_events": Fake_Events(
#     num_users = os.getenv("NUM_USERS"),
#     num_products = os.getenv("NUM_PRODUCTS"),
#     min_sleep=  os.getenv("MIN_SLEEP"),
#     max_sleep=  os.getenv("MAX_SLEEP")
#     )
#     }
#     return config
load_dotenv()
num_users = os.getenv("NUM_USERS")
num_products = os.getenv("NUM_PRODUCTS")
min_sleep=  os.getenv("MIN_SLEEP")
max_sleep=  os.getenv("MAX_SLEEP")

print(num_users, num_products, min_sleep, max_sleep)