from django.db import models

from distutils.command.upload import upload
from email.policy import default
from enum import unique
from pyexpat import model
from django.db import models

# Create your models here.


class Maincategory (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    maincategory = models.ForeignKey(Maincategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default="In Stock", null=True)
    size = models.CharField(max_length=20, default="in Stock", null=True)
    stock = models.CharField(
        max_length=20, default="In Stock", null=True, blank=True)
    descripton = models.TextField()
    baseprice = models.IntegerField()
    discount = models.IntegerField(default=0, null=True, blank=True)
    finalprice = models.IntegerField()
    pic1 = models.ImageField(upload_to="uploads", default="", null=True)
    pic2 = models.ImageField(upload_to="uploads", default="", null=True)
    pic3 = models.ImageField(upload_to="uploads", default="", null=True)
    pic4 = models.ImageField(upload_to="uploads", default="", null=True)

    def __str__(self):
        return self.name


# class Buyer(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(max_length=50)
#     phone = models.CharField(max_length=15)
#     addressline1 = models.CharField(max_length=150)
#     addressline1 = models.CharField(max_length=150)
#     addressline1 = models.CharField(max_length=150)
#     pin = models.CharField(max_length=10)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     pic4 = models.FileField(upload_to="uploads", default="", null=True)

#     def __str__(self):
#         return str(self.id)+" "+self.username
    # from django.db import models

class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    # Allow null values for email
    email = models.EmailField(max_length=50, null=True)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=150,)
    addressline2 = models.CharField(
        max_length=150, default='')  # Corrected field name
    addressline3 = models.CharField(
        max_length=150, default='')  # Corrected field name
    pin = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    profile_picture = models.FileField(upload_to="uploads", default="", null=True)

    def __str__(self):
        return str(self.id) + " " + self.username
