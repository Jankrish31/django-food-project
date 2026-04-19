from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.foodDetails, name='foodDetails'),
    path('add-cart/<int:id>/', views.add_cart, name='add_cart'),
    path('cart/', views.cart, name='cart'),
    path("customize/<int:id>/", views.customize, name="customize"),
    path('cart/delete/<int:food_id>/', views.delete_cart, name='delete_cart'),
    path('order/', views.order_food, name='order'), 
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('bill/', views.billtemplate, name='billtemplate'),

]

