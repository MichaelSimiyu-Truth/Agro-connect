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
    cart_items = cart.cartitem_set.all()  # Fetch all items in the cart
    
    context = {
        'cart': cart,
        'cart_items': cart_items  # Pass cart items to the template
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

# views.py
@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
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

# views.py

# views.py

import base64
import requests
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = settings.MPESA_AUTH_URL
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {encoded_credentials}'}

    response = requests.get(api_url, headers=headers)
    json_response = response.json()
    return json_response.get('access_token', '')

def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_mpesa_access_token()
    api_url = settings.MPESA_API_URL
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode('utf-8')).decode('utf-8')
    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': settings.MPESA_SHORTCODE,
        'PhoneNumber': phone_number,
        'CallBackURL': settings.MPESA_CALLBACK_URL,
        'AccountReference': 'CompanyXLTD',
        'TransactionDesc': 'Payment of X'
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

@csrf_exempt
def mpesa_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')

        if not phone_number or not amount:
            return JsonResponse({'error': 'Invalid input'}, status=400)

        response = lipa_na_mpesa_online(phone_number, amount)
        return JsonResponse(response)

    return render(request, 'checkout.html')

@csrf_exempt
def mpesa_callback(request):
    # Handle the callback from M-Pesa here
    data = request.body
    print(data)
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


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
