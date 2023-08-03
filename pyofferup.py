import logging
import json

from lib.offerup import get_feed, get_details
from models import *

logging.basicConfig(level=logging.INFO)

def get_listings(loc: str) -> [OUListing]:
    feed_resp = get_feed(loc)
    # Filter out some empty or ad-based tiles
    tiles_resp = [t for t in feed_resp if t.get('__typename', 'INVALID') == "ModularFeedTileListing"]
    # and the extraneous bookeeping
    listings_resp = [l['listing'] for l in tiles_resp ]

    def listing_hook(obj):
        if obj['__typename'] == 'ModularFeedListing':
            return OUListing(**obj)
        return obj

    return json.loads(json.dumps(listings_resp), object_hook=listing_hook)

def get_listing_details_from_id(id: str) -> OUListingDetail:
    details_resp = get_details(id)
    
    def detail_hook(obj):
        if obj['__typename'] == 'Listing':
            return OUListingDetail(**obj)
        return obj

    return json.loads(json.dumps(details_resp), object_hook=detail_hook)