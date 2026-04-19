from django.db import models
from django.contrib.auth.models import User



#create my models
Catogeries =[
    {"BRIYANI","Briyani"},
    {"PAROOTA","Paroota"},
    {"CHICKENRICE","Chickenrice"},
    {"CHICKENOODLES","Chickennoodles"},
    {"CHAPPAATI","Chappati"},
    {"DOSA","dosa"},
    {"IDLY","Idly"},
    {"POORI","Poori"},
    {"PONGAL","Pongal"},
    {"IDIYAPPAM","Idiyappam"},
    {"KICHIDI","kichidi"},
    {"UPUMA","upuma"}
]
# Create your models here.

class FoodItems(models.Model):
    foodname = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    rating = models.FloatField()
    food_img = models.ImageField(upload_to='food_images/')
    catogery = models.CharField(max_length=50)
    
    def __str__(self):
        return self.foodname
    




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foodname = models.CharField(max_length=200)
    price = models.FloatField()
    rating = models.FloatField()
    food_img = models.ImageField(upload_to='food_images/')
    catogery = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.foodname} ({self.user.username})"



class Size(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    size_type = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.food.foodname} - {self.size_type}"
    
class BaseType(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    base_name = models.CharField(max_length=100)
    base_img = models.ImageField(upload_to='base/', blank=True, null=True)

    def __str__(self):
        return f"{self.food.foodname} - {self.base_name}"
    
class Topping(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    topping_img = models.ImageField(upload_to='topping/', blank=True, null=True)

    def __str__(self):
        return f"{self.food.foodname} - {self.name}"

class Sauce(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    sauce_img = models.ImageField(upload_to='sauce/', blank=True, null=True)

    def __str__(self):
        return f"{self.food.foodname} - {self.name}"
    

   



    

    
    






    
