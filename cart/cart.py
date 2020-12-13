from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    """
    Initialize the cart object.
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart: # If cart is not present in the session, create a new one
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add or update product quantity
        * Using product_id as key to make sure same product isn't added twice.
        * Django uses JSON to serialize session data, hence converting product_id to string. (JSON keys can be strings only)
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
            
    def save(self):
        # Marked as modified to make sure changes are made
        self.session.modified = True
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            # Add quantity back to database
            product.quantity += self.cart[product_id]['quantity']
            del self.cart[product_id]
            product.save()
            self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """
        Remove cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def __iter__(self):
        """
        Create an iterator object to facilitate iteration over cart items
        and get the products from database. Required for rendering products in template.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        # Copy current cart object
        cart = self.cart.copy()
        # Add product istances to the cart
        for product in products:
            cart[str(product.id)]['product'] = product
        # Iterate over cart items, converting price to Decimal and adding 'total_price' attribute
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    

    def __len__(self):
        """
        Return the number of items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())
