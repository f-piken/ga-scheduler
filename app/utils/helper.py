import random

def random_vehicle(vehicles):
    return random.choice(vehicles)

def random_driver(drivers):
    return random.choice(drivers)

def random_time(times):
    return random.choice(times)

def split_jamaah(jamaah, size=10):
    return [jamaah[i:i+size] for i in range(0, len(jamaah), size)]