from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Artist(models.Model):
    Id_Artist = models.AutoField(primary_key=True)
    Artist_Name = models.CharField(max_length=200, unique=True)
    country_choices = [
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('PE', 'Peru'),
        ('JA', 'Japan')
    ]
    Artist_Country = models.CharField(max_length=3, choices=country_choices, default='US')

class Album(models.Model):
    Id_Album = models.AutoField(primary_key=True)
    Id_Artist = models.ForeignKey(to=Artist, on_delete=models.RESTRICT, db_column='Id_Artist')
    Album_Name = models.CharField(max_length=200)
    genre_choices = [
        ('roc', 'Rock'),
        ('pop', 'Pop'),
        ('hip', 'Hip-hop'),
        ('edm', 'EDM')
    ]
    Album_MainGenre = models.CharField(max_length=3, choices=genre_choices, default='roc')
    Album_Price = models.DecimalField(max_digits=6, decimal_places=2)
    Album_Cover_Path = models.CharField(max_length=100, default='imgs/covers/mami.jpeg')

class Order(models.Model):
    Id_Order = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='User')
    Order_Date = models.DateTimeField(auto_now_add=True)

class Order_Detail(models.Model):
    Id_OrderDetail = models.AutoField(primary_key=True)
    Id_Order = models.ForeignKey(to=Order, on_delete=models.CASCADE, db_column='Id_Order')
    Id_Album = models.ForeignKey(to=Album, on_delete=models.RESTRICT, db_column='Id_Album')
    Quantity = models.IntegerField()
