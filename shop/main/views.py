from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 
import logging
from .models import Cart, Product, ProductImage, Order, CartItem, OrderItem
from .forms import ProductForm, CartAddProductForm, CartAddProductForm
from datetime import timedelta
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/track_order.html', {'order': order})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.remove(cart_item)
    cart_item.delete()
    return redirect('cart')

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = sum(item.product.price * item.quantity for item in order.items.all())
    return render(request, 'main/order_confirmation.html', {'order': order, 'total_price': total_price})


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', 'Unknown')
        last_name = request.POST.get('last_name', 'Unknown')
        email = request.POST.get('email', 'example@example.com')
        delivery_service = request.POST.get('delivery_service', 'novaposhta')
        delivery_type = request.POST.get('delivery_type')
        branch_number = request.POST.get('branch_number') or 0
        postal_index = request.POST.get('postal_index', '00000')
        store_number = request.POST.get('store_number', '000')
        address = request.POST.get('address', 'Не указано')
        postamat_number = request.POST.get('postamat_number', '000')

        # Получаем значение seller из БД продукта
        if cart_items.exists():
            seller = cart_items.first().product.owner
        else:
            seller = None

        order = Order.objects.create(
            user=request.user,
            seller=seller,
            first_name=first_name,
            last_name=last_name,
            email=email,
            delivery_service=delivery_service,
            delivery_type=delivery_type,
            branch_number=branch_number,
            postal_index=postal_index,
            store_number=store_number,
            address=address,
            postamat_number=postamat_number
        )
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.quantity -= item.quantity
            item.product.save()
        order.save()
        cart_items.delete()
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'main/checkout.html', {'cart_items': cart_items})



def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user

            # Обновление количества товара
            product.quantity = request.POST.get('quantity')
            product.save()

            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                if image:
                    if i == 0:
                        product.image1 = image
                    elif i == 1:
                        product.image2 = image
                    elif i == 2:
                        product.image3 = image
                    elif i == 3:
                        product.image4 = image
                    elif i == 4:
                        product.image5 = image
                    elif i == 5:
                        product.image6 = image
                    elif i == 6:
                        product.image7 = image
                    elif i == 7:
                        product.image8 = image
            product.save()
            return redirect('details', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    images = [
        product.image1, product.image2, product.image3, product.image4,
        product.image5, product.image6, product.image7, product.image8
    ]

    return render(request, 'main/edit_product.html', {
        'form': form,
        'product': product,
        'images': images,
        'image_range': range(1, 9)
    })



def delete_image(request, product_id, image_index):
    product = get_object_or_404(Product, id=product_id)
    field_name = f'image{image_index}'

    # Удаляем изображение
    setattr(product, field_name, None)
    product.save()

    return redirect('edit_product', product_id=product.id)


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, owner=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('my_products')
    return render(request, 'main/delete_product.html', {'product': product})


@login_required
def my_products(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, 'main/my_products.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                # Запоминаем пользователя на 30 дней
                request.session.set_expiry(timedelta(days=30))
            else:
                # Закрываем сессию при закрытии браузера
                request.session.set_expiry(0)
            return redirect('/profile')
        else:
            messages.error(request, 'Такой пользователь не зарегистрирован')
    return render(request, 'main/login.html')



def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    new_quantity = int(request.POST.get('quantity', cart_item.quantity))
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.quantity >= quantity:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart.items.add(cart_item)
        cart_item.quantity += quantity
        cart_item.save()

        # Обновим количество товара на складе
        product.quantity -= quantity
        product.save()

        messages.success(request, 'Товар добавлен в корзину.')
        return redirect('cart')
    else:
        messages.error(request, 'Товар недоступен для заказа в таком количестве.')
        return redirect('product')

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product.html', {'products': products})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            images = request.FILES.getlist('images')
            if not images:
                print("No images received")
            for i, image in enumerate(images):
                if image:
                    if i == 0:
                        product.image1 = image
                    elif i == 1:
                        product.image2 = image
                    elif i == 2:
                        product.image3 = image
                    elif i == 3:
                        product.image4 = image
                    elif i == 4:
                        product.image5 = image
                    elif i == 5:
                        product.image6 = image
                    elif i == 6:
                        product.image7 = image
                    elif i == 7:
                        product.image8 = image
                    product.save()
                    print(f"Image {i+1} uploaded: {image.name}")
                else:
                    print("Empty image file")
            return redirect('product')
        else:
            print("Form errors: ", form.errors)
    else:
        form = ProductForm()
    return render(request, 'main/create_product.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = name
                    user.last_name = surname
                    user.save()
                    login(request, user)
                    return redirect('/profile')
                else:
                    messages.error(request, 'Пользователь с таким email уже существует')
            else:
                messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            messages.error(request, 'Пароли не совпадают')
    
    return render(request, 'main/reg.html')


def logout_view(request):
    logout(request)
    return redirect('home') 

def home_view(request):
    products = Product.objects.all()
    return render(request, "main/index.html", {'products': products})

def reg(request):
    return render(request, "main/reg.html")

def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'orders': orders})

def prodavec(request):
    return render(request, "main/prodavec.html")

def details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'main/details.html', {'product': product})

def my_orders(request):
    orders = Order.objects.filter(seller=request.user)
    return render(request, 'main/orders.html', {'orders': orders})

def update_order_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'оплачен'
    order.save()
    return redirect('my_orders')

def update_order_shipped(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'доставляется'
    order.save()
    return redirect('my_orders')

def update_order_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'доставлен'
    order.save()
    return redirect('my_orders')


