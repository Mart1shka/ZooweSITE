from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import cart_view, checkout, order_confirmation

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cart', views.cart_view, name='cart'),
    path('product', views.product_list, name='product'),
    path('login', views.login_view, name='login'),
    path('reg', views.register_view, name='register'),
    path('profile', views.profile, name='profile'),
    path('prodavec/', views.prodavec, name='prodavec'),
    path('logout/', views.logout_view, name='logout'),  
    path('details/<int:product_id>/', views.details, name='details'),
    path('create_product', views.create_product, name='create_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('my_products/', views.my_products, name='my_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete_image/<int:product_id>/<int:image_index>/', views.delete_image, name='delete_image'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('track_order/<int:order_id>/', views.track_order, name='track_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('update_order_paid/<int:order_id>/', views.update_order_paid, name='update_order_paid'),
    path('update_order_shipped/<int:order_id>/', views.update_order_shipped, name='update_order_shipped'),
    path('update_order_delivered/<int:order_id>/', views.update_order_delivered, name='update_order_delivered'),



] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
