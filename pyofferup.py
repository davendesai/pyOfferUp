import logging
import json

from lib.offerup import get_feed, get_details
from models import *

logging.basicConfig(level=logging.INFO)

def get_listings(loc: str) -> [OUListing]:
    feed = get_feed(loc)
    # Filter out some empty or ad-based tiles
    tiles = [t for t in feed if t.get('__typename', 'INVALID') == "ModularFeedTileListing"]
    # and the extraneous bookeeping
    listings = [l['listing'] for l in tiles ]

    return json.loads(json.dumps(listings), object_hook=lambda l: OUListing(**l))

def get_listing_details_from_id(id: str) -> OUListingDetail:
    details = get_details(id)
    return json.loads(json.dumps(details), object_hook=lambda d: OUListingDetail(**d))