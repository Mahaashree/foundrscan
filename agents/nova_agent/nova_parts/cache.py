import json
import os

CACHE_PATH = "market_cache.json"

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def get_from_cache(idea_key):
    cache = load_cache()
    return cache.get(idea_key, None)

def store_to_cache(idea_key, data):
    cache = load_cache()
    cache[idea_key] = data
    save_cache(cache)
