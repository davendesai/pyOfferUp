import logging
import sys
import json

from lib.offerup import get_feed
from models.OUListing import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout = logging.StreamHandler(sys.stdout)
stdout.setFormatter(logging.Formatter("%(name)s: %(message)s"))
logger.addHandler(stdout)

def get_listings(loc: str) -> [OUListing]:
    feed = get_feed("Seattle, WA")

    def listing_hook(obj):
        if 'tileId' in obj.keys():
            return obj['listing']
        if 'listingId' not in obj.keys():
            return obj
        return OUListing(**obj)

    return json.loads(json.dumps(feed), object_hook=listing_hook)

def get_details(id: str):
    pass

