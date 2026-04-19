from django.urls import path
from learnapp import views

urlpatterns = [

   path('',views.registration,name="register"),
    path('login',views.user_login,name="login"),
    path('home',views.home,name="home"),
    path('logout',views.user_logout,name='logout'),
    path('profile',views.userprofile,name='profile'),
    path('update',views.userupdate,name='update'),
    path('AllFoods',views.AllFoods,name='AllFoods'),
    path('addnewfood',views.addnewfood,name='addnewfood'),
    path('cart', views.Cart, name='cart'),

]