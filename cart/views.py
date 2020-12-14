from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.conf import settings
import stripe

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    Cart page. Allows modifying product quantity within cart page.
    """
    cart = Cart(request)
    total = cart.get_total_price()
    for item in cart:
        form_data = {'quantity': item['quantity'], 'override': True}
        item['update_quantity_form'] = CartAddProductForm(initial=form_data)
    context = {'cart': cart}
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Online Shop - New order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    context = {'total': total,'data_key':data_key, 'stripe_total':stripe_total, 'description':description}
    return render(request, 'cart/detail.html', context )
    if request.method == 'POST':
        print(request.POST)
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']

            customer = stripe.Customer.create(
                        email=email,
                        source = token
            )
            charge = stripe.Charge.create(
                        amount=stripe_total,
                        currency="eur",
                        description=description,
                        customer=customer.id
            )
        except stripe.error.CardError as e:
            return false, e