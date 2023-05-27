from home.models import Product

SESSION_KEY = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_KEY)
        if not cart:
            cart = self.session[SESSION_KEY] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product # without any thing it returns str method
        
        for value in cart.values():
            value['total_price'] = value['quantity'] * int(value['price'])
            yield value

    def __len__(self):
        return sum(value['quantity'] for value in self.cart.values())
    
    def cart_add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save() 

    def remove_cart(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] == 0:
                del self.cart[product_id]
        self.save()

    def save(self):
        self.session.modified = True
    
    def get_total_price(self):
        return sum(value['total_price'] for value in self.cart.values())
    
    def clear(self):
        del self.session[SESSION_KEY]
        self.save()