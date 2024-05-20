from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    email = models.EmailField(unique = True, max_length=30)
    name = models.CharField(max_length = 30)
    contact = models.CharField(max_length = 12)
    password = models.CharField(max_length = 30)
    picture = models.ImageField(upload_to="picture/", default="")
    role_case = [
        ('buyer','buyer'),
        ('seller','seller'),
    ]
    role = models.CharField(max_length = 20 , choices = role_case)

    def __str__(self):
        return self.name + " || " + self.contact
    
class Product(models.Model):
    categorie = (
        ("Men","Men"),
        ("Women","Women"),
        ("Chiled","Chiled"),
    )

    size = (
        ("S","S"),
        ("L","L"),
        ("M","M"),
        ("XL","XL"),
        ("XXL","XXL"),
    )

    brand = (
        ("Levi's","Levi's"),
        ("Being Human","Being Human"),
        ("Biba","Biba"),
        ("Aurelia","Aurelia"),
        ("Max","Max"),
    )

    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    categorie = models.CharField(max_length = 20 ,choices = categorie ,null = True)
    size = models.CharField(max_length = 20 ,choices = size ,null = True)
    brand = models.CharField(max_length = 20 ,choices = brand ,null = True)
    pname = models.CharField(max_length = 20)
    ppicture = models.ImageField(upload_to = "ppicture/" , default="")
    disc = models.TextField()
    pprice = models.IntegerField()

    def __str__(self):
        return self.pname + ' || ' + self.user_id.name
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)

    def __str__(self):
        return self.product.pname + ' || ' + self.user.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1)  
    cart_price =  models.PositiveIntegerField()
    total_price = models.PositiveSmallIntegerField(default=0)
    pyment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name + " || " + self.product.pname 
    
class Order_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.PositiveBigIntegerField()

    def __str__(self):
        return self.user.name + " || " + self.address