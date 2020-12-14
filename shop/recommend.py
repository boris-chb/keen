import redis
from django.conf import settings
from .models import Product

# Connect to Redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

class Recommendations():
    
    # Build Redis key formatted <product:[id]:purchased_with>.
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'
    
    def bought_together(self, products: list): # List of products that belong to the same order
        product_ids = [p.id for p in products] # List of IDs
        for product_id in product_ids: # Pick a product ID
            for with_id in product_ids: # Pick another product ID to compare against
                if product_id != with_id: # Make sure it's not same product
                    # Get Redis key for given product
                    product_key = self.get_product_key(product_id)
                    # Increment their score by 1
                    r.zincrby(product_key, 1, with_id)
    
    def suggest_products_for(self, products: list, max_results=6):
        """
            Takes in a list of Product objects to get recommendations for.
            max_results = number of desired recommendations.
        """
        
        product_ids = [p.id for p in products]
        if len(products) == 1: # Only 1 product
            # Retrieve the ID of products bought together
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1,
                                   desc=True)[:max_results]
        else:
            # Generate temporary key using IDs of products
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # Combine score of all products
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # Remove IDs for the products the recommendations are for
            r.zrem(tmp_key, *product_ids)
            # Get product IDs by their score, descending
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            # Remove the temporary key
            r.delete(tmp_key)
        
        suggested_product_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products
    
    def clean_up(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
            