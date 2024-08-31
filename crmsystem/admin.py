from django.contrib import admin
from .models import Customer, Date, Invoice, Position, PositionDefinition, ProductDefinition, Anamnese

# Register your models here.
admin.site.register(Customer)
admin.site.register(Date)
admin.site.register(Invoice)
admin.site.register(Position)
admin.site.register(PositionDefinition)
admin.site.register(ProductDefinition)
admin.site.register(Anamnese)