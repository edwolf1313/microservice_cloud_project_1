from django.db import models

# Create your models here.
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

class chart_user_data(models.Model):
    """ untuk menyimpan chart dari produk yang ditambahkan user """
    payment = models.DecimalField(max_digits=65, decimal_places=0, blank=False)
    quantity = models.IntegerField(default=1 ,validators=[MinValueValidator(1), MaxValueValidator(100)], blank=False)
    product_id = models.CharField( max_length=100, blank=False )
    client_id = models.CharField( max_length=100, blank=False )
    created_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
