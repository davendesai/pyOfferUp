from pyofferup import get_listings

listings = get_listings("Seattle, WA")

for l in listings[:3]:
    print(l.get_url())