from django.contrib import admin
from .models import FoodItems


# Register your models here.
admin.site.register(FoodItems)
from .models import Size,BaseType,Topping,Sauce


admin.site.register(Size)
admin.site.register(BaseType)
admin.site.register(Topping)
admin.site.register(Sauce)


