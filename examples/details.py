from pyofferup import *

listings = get_listings("Seattle, WA")
first_listing = listings[0]

details = get_listing_details_from_id(first_listing.listingId)

print(details.id, details.title, "$"+details.price)
