from django.shortcuts import render,get_object_or_404
from foods.models import FoodItems,Cart,User
from foods.utils import send_email_view
from .models import FoodItems, Size, BaseType, Topping, Sauce
from datetime import datetime
from .models import Cart
from datetime import datetime
from .utils import send_email_view
from django.conf import settings
from datetime import datetime
import pytz


def home(request):
    return render(request, "home.html")

# Create your views here.
def foodDetails(request,id=0):
    foodsitems = FoodItems.objects.get(id=id)
    return render(request,"foods/foodDetails.html",
    {'foodsitems':foodsitems})


from django.shortcuts import render, get_object_or_404, redirect

def customize(request, id):
    food = get_object_or_404(FoodItems, id=id)

    sizes = Size.objects.filter(food=food)
    bases = BaseType.objects.filter(food=food)
    toppings = Topping.objects.filter(food=food)
    sauces = Sauce.objects.filter(food=food)

    if request.method == "POST":
        size_id = request.POST.get('size')
        base_id = request.POST.get('base')
        topping_ids = request.POST.getlist('toppings')
        sauce_ids = request.POST.getlist('sauces')

        print("SIZE:", size_id)
        print("BASE:", base_id)
        print("TOPPINGS:", topping_ids)
        print("SAUCES:", sauce_ids)

        return redirect('AllFoods')

    context = {
        'foodsitems': food,
        'sizes': sizes,
        'bases': bases,
        'toppings': toppings,
        'sauces': sauces,
    }

    return render(request, 'customize.html', {
        'food': food,
        'bases': bases,
        'sizes': sizes,
        'toppings': toppings,
        'sauces': sauces,
    })



def cart(request):
    foodsitems = request.session.get('cart', [])


    total_price = sum(item.get('price', 0) for item in foodsitems)

    context = {
        'foodsitems': foodsitems,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)



def add_cart(request, id):  
    from django.shortcuts import get_object_or_404
    food = get_object_or_404(FoodItems, id=id)

    cart = request.session.get('cart', [])

   
    for item in cart:
        if item['food_id'] == food.id:
            item['quantity'] += 1
            break
    else:
        cart.append({
            'food_id': food.id,
            'foodname': food.foodname,
            'price': food.price,
            'quantity': 1,
            'image': food.food_img.url if food.food_img else '',
            'description': food.description,
            'base': getattr(food, 'base', ''),
            'size': getattr(food, 'size', ''),
            'toppings': getattr(food, 'toppings', ''),
            'sauces': getattr(food, 'sauces', ''),
        })

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', [])
    total_price = sum(item['price'] * item.get('quantity', 1) for item in cart)

    context = {
        'foodsitems': cart,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def delete_cart(request, food_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['food_id'] != food_id]
    request.session['cart'] = cart
    return redirect('cart')



def order_food(request):
  
    cart = request.session.get('cart', [])

    total_items = sum(item.get('quantity', 1) for item in cart)

    total_amount = 0
    for item in cart:
        qty = item.get('quantity', 1)
        price = item.get('price', 0)
        total_amount += qty * price

   
    request.session['total_amount'] = total_amount

    context = {
        'cart_items': cart,
        'total_items': total_items,
        'total_amount': total_amount, 
    }

    return render(request, 'order.html', context)




def payment(request):
    

    total_amount = request.session.get('total_amount', 0)

    return render(request, 'payment.html', {
        'total_amount': total_amount
    })





def payment_success(request):

    cart = request.session.get('cart', [])

    if not cart:
        return redirect('cart')

    total_amount = sum(item['price'] * item['quantity'] for item in cart)

    bill_data = {
    'items': cart,
    'total_amount': total_amount,
    'total_items': sum(item['quantity'] for item in cart),
    'order_id': f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
    'order_date': datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
}

    request.session['bill_data'] = bill_data

    email = request.user.email if request.user.is_authenticated else "pavithrasree994@gmail.com"

    send_email_view(email, bill_data)

    request.session['cart'] = []

    return render(request, 'payment_success.html', {
        'total_amount': total_amount
    })

# ------------------ BILL PAGE ------------------

def billtemplate(request):

    bill_data = request.session.get('bill_data')

    if not bill_data:
        return redirect('cart')

    # ⭐ ADD image_url for browser display
    for item in bill_data['items']:
        if item.get('image'):
            item['image_url'] = settings.MEDIA_URL + item['image']

    return render(request, 'billtemplate.html', bill_data)
