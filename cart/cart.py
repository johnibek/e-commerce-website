from store.models import Product, Profile

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key, create one.
        if not cart:
        # if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site

        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass

        else:
            self.cart[product_id] = int(product_qty)

        self.save()

        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_profile.update(old_cart=carty)

    def add(self, product, quantity):
        print(product)
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass

        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.save()

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)  # "{'3':1, '2':4}"
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=carty)

    def save(self):
        # Mark the session as modified to make sure it gets saved
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        print(self.cart)
        # Get ids from cart
        product_ids = self.cart.keys()

        # use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)

        return products

    def get_quants(self):
        return self.cart

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        cart = self.cart

        cart[product_id] = product_qty

        self.save()

        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_profile.update(old_cart=carty)

        return cart

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_profile.update(old_cart=carty)

    def total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for key, value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)

        return total
