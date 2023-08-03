
class OUListing:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_url(self) -> str:
        return "http://offerup.com/item/detail/" + self.listingId