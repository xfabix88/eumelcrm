from django.db import models
from datetime import datetime, date

class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, blank=True) 
    birthday = models.CharField(max_length=50, blank=True) 
    mail = models.CharField(max_length=100, blank=True) 
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    street =models.CharField(max_length=100, blank=True)
    housenumber = models.CharField(max_length=50, blank=True)
    plz = models.CharField(max_length=15, blank=True) 
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    diagnose = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class Claims(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    category= models.CharField(max_length=100)
    customer_id = models.CharField(max_length=100)

    def __str__(self):
        return (f"{self.customer_id} {self.category}")
    

class PositionDefinition(models.Model):

    PRODUKT = (('B30', 'Bioresonanz 30 Minuten'),
            ('B60', 'Bioresonanz 60 Minuten'),
            ('B90', 'Bioresonanz 90 Minuten'),
            ('P60', 'Psychotherapie 60 Minuten'),
            ('P90', 'Psychotherapie 90 Minuten'),
            ('E01', 'Erstgespräch')
            )

    product = models.CharField(max_length=100,blank=True, choices=PRODUKT)
    number = models.CharField(max_length=250)
    description = models.CharField(max_length=255, blank='True')
    price = models.IntegerField(default=20)
    count = models.IntegerField(default=1)
    factor = models.DecimalField(default=1.0, decimal_places=1, max_digits=4)

    def __str__(self):
        return (f"{self.id} {self.product} {self.number} {self.description}") 
    
class ProductDefinition(models.Model):
    number = models.CharField(max_length=250)
    description = models.CharField(max_length=255, blank='True')
    category = models.CharField(max_length=250)

    def __str__(self):
        return (f"{self.id} {self.number} {self.description}") 
      
    

class Anamnese(models.Model):

    text = models.TextField()
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    product = models.ForeignKey('ProductDefinition',on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.id} {self.customer} {self.product}")  

    
class Date(models.Model):
    PRODUKT = (('B30', 'Bioresonanz 30 Minuten'),
            ('B60', 'Bioresonanz 60 Minuten'),
            ('B90', 'Bioresonanz 90 Minuten'),
            ('P60', 'Psychotherapie 60 Minuten'),
            ('P90', 'Psychotherapie 90 Minuten'),
            ('E01', 'Erstgespräch')
            )


    created_at = models.DateTimeField(auto_now_add=True)
    product = models.CharField(max_length=100,blank=True, choices=PRODUKT)
    note = models.TextField(max_length=100, blank=True) 
    customer = models.CharField(max_length=100, blank=True) 
    day = models.DateField(default="2024-05-22", blank=True)
    time_begin = models.TimeField(default="10:00", blank=True)
    time_end = models.TimeField(default="11:00", blank=True)
  
    text = models.TextField(max_length=10000, blank=True)
    googlecalendar = models.CharField(max_length=1000, blank=True) 
    invoice = models.CharField(max_length=100, blank=True) 
        
    def __str__(self):
        return (f"{self.id}{self.customer}")
    
    """ day = models.DateField(max_length=100, blank=True)
    time_begin = models.DateTimeField(max_length=100, blank=True)
     dino = models.ForeignKey(Customer, blank=True, on_delete=models.CASCADE)
    time_end = models.DateTimeField(max_length=100, blank=True) """



class Invoice(models.Model):

    STATUS = (('offen', 'offen'),
            ('bezahlt', 'bezahlt'),
             ('storniert', 'storniert'),
             ('fällig', 'fällig')
            )

    number = models.CharField(max_length=100, blank=True) 
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    date_begin = models.DateField(default="2024-05-22", blank=True)
    date_end = models.DateField(default="2024-05-22", blank=True)
    product= models.CharField(max_length=100, blank=True) 
    text = models.CharField(max_length=100, blank=True) 
    price = models.CharField(max_length=100, blank=True) 
    status = models.CharField(max_length=100, default='offen',blank=True, choices=STATUS) 
    show_diagnose = models.BooleanField(blank=True, default='False') 
    already_paid = models.BooleanField(blank=True, default='False') 

    reci_title = models.CharField(max_length=20, blank=True)
    reci_first_name = models.CharField(max_length=100)
    reci_last_name = models.CharField(max_length=100)
    reci_street =models.CharField(max_length=100, blank=True)
    reci_housenumber = models.CharField(max_length=50, blank=True)
    reci_plz = models.CharField(max_length=15, blank=True) 
    reci_city = models.CharField(max_length=100, blank=True)
    reci_country = models.CharField(max_length=50, blank=True)


    def __str__(self):
            return (f"{self.id} {self.number}")
    
    @property
    def is_past_due(self):
        return date.today() > self.date_begin
    
class Position(models.Model):

    GEBPOS = ((
         '21.1', '21.1'),
        ('21.2', '21.2'),
        )


    number = models.CharField(max_length=250)
    description = models.CharField(max_length=255)
    price = models.IntegerField(default=20)
    count = models.IntegerField(default=1)
    endprice = models.CharField(max_length=255)
    factor = models.DecimalField(default=1.0, decimal_places=1, max_digits=4)
    date = models.ForeignKey('Date',on_delete=models.CASCADE)


    def __str__(self):
            return (f"{self.number} {self.description}")
    
    @property
    def endprice2(self):
        endprice2 = int(self.count) * self.factor * int(self.price)
        return endprice2