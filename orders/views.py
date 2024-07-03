from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Cart, CartItem
from .forms import OrderCreateForm
from products.models import Product
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.farmer = request.user
            order.save()
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            cart.cartitem_set.all().delete()  # Clear the cart after creating the order

            stripe_token = request.POST.get('stripeToken')
            if stripe_token:
                try:
                    charge = stripe.Charge.create(
                        amount=int(order.get_total_cost() * 100),  # Amount in cents
                        currency='usd',
                        description='Order {}'.format(order.id),
                        source=stripe_token
                    )
                    order.status = 'Paid'
                    order.save()
                    return redirect('order_list_view')
                except stripe.error.StripeError as e:
                    # Handle error
                    order.delete()
                    return render(request, 'checkout.html', {'cart': cart, 'form': form, 'error': str(e)})
    else:
        form = OrderCreateForm()
    return render(request, 'checkout.html', {'cart': cart, 'form': form, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

@login_required
def order_list_view(request):
    orders = Order.objects.filter(farmer=request.user)
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, farmer=request.user)
    return render(request, 'order_detail.html', {'order': order})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return JsonResponse({'status': 'success'}, status=200)

def handle_checkout_session(session):
    order_id = session['client_reference_id']
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'Paid'
        order.save()
    except Order.DoesNotExist:
        pass



'''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Cart, CartItem
from .forms import OrderCreateForm
from products.models import Product
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Cart, OrderItem, Order
from .forms import OrderCreateForm

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')


def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.farmer = request.user
            order.save()
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            cart.cartitem_set.all().delete()  # Clear the cart after creating the order

            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),  # Amount in cents
                    },
                    'quantity': item.quantity,
                } for item in order.orderitem_set.all()],
                mode='payment',
                success_url=request.build_absolute_uri(redirect('order_list_view')),
                cancel_url=request.build_absolute_uri(redirect('checkout_view')),
            )
            return redirect(session.url, code=303)
    else:
        form = OrderCreateForm()
    return render(request, 'checkout.html', {'cart': cart, 'form': form})
@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.farmer = request.user
            order.save()
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            cart.cartitem_set.all().delete()  # Clear the cart after creating the order
            return redirect('order_list_view')
    else:
        form = OrderCreateForm()
    return render(request, 'checkout.html', {'cart': cart, 'form': form})

@login_required
def order_list_view(request):
    orders = Order.objects.filter(farmer=request.user)
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, farmer=request.user)
    return render(request, 'order_detail.html', {'order': order})

# views.py
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return JsonResponse({'status': 'success'}, status=200)

def handle_checkout_session(session):
    order_id = session['client_reference_id']
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'Paid'
        order.save()
    except Order.DoesNotExist:
        pass
'''
