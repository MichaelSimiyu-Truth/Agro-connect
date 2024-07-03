


from django.shortcuts import render, redirect
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageForm
from django.contrib.auth.decorators import login_required

@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.supplier = request.user
            product.save()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)
            return redirect('product_list')
    else:
        product_form = ProductForm()
    return render(request, 'add_product.html', {'product_form': product_form})

@login_required
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('product_list')
    else:
        product_form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'product_form': product_form})

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_list')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})






'''@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.supplier = request.user
            product.save()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)
            return redirect('product_list')
    else:
        product_form = ProductForm()
    return render(request, 'products/add_product.html', {'product_form': product_form})

@login_required
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('product_list')
    else:
        product_form = ProductForm(instance=product)
    return render(request, 'products/update_product.html', {'product_form': product_form})

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_list')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})'''