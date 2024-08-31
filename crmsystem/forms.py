from django import forms 
from datetime import datetime
from .models import Customer, Date, Invoice, Position, Anamnese, ProductDefinition


class AddCustomerForm(forms.ModelForm):
    geschlecht = (('männlich', 'männlich'),('weiblich', 'weiblich'),)
    title = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Titel", "class": "form-control"}), label="")
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Vorname", "class": "form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Nachname", "class": "form-control"}), label="")
    sex = forms.ChoiceField(required=False, widget=forms.widgets.Select(attrs={"placeholder":"männlich", "class": "form-control"}), label="", choices=geschlecht)
    birthday = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Geburtstag", "class": "form-control"}), label="")
    mail = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"eMail", "class": "form-control"}), label="")
    phone = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Festnetz", "class": "form-control"}), label="")
    mobile = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Handy", "class": "form-control"}), label="")
    street =forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Straße", "class": "form-control"}), label="")
    housenumber = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Hausnummer", "class": "form-control"}), label="")
    plz = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"PLZ", "class": "form-control"}), label="")
    city = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Ort", "class": "form-control"}), label="")
    country = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Land", "class": "form-control"}), label="")

    class Meta:
        model = Customer
        exclude =('user', 'diagnose')

class AddCustomerDiagnoseForm(forms.ModelForm):

    diagnose = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder":"Text", "class": "form-control", "rows":"10"}), label="")

    class Meta:
        model = Customer
        fields =('diagnose',)

class AddAnamneseForm(forms.ModelForm):

    text = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder":"Text", "class": "form-control", "rows":"50"}), label="")
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(),required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")
    product = forms.ModelChoiceField(queryset=ProductDefinition.objects.values_list('category',flat=True).distinct(),required=False, widget=forms.widgets.Select(attrs={"placeholder":"Text", "class": "form-control"}), label="")

    class Meta:
        model = Anamnese
        fields =('product','text','customer')

class UpdateAnamneseForm(forms.ModelForm):

    text = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder":"Text", "class": "form-control", "rows":"50"}), label="")
    customer = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")
    product = forms.ModelChoiceField(queryset=ProductDefinition.objects.all(),required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")

    class Meta:
        model = Anamnese
        fields =('product','text',)


class AddCalenderForm(forms.ModelForm):


    PRODUKT = (('B30', 'Bioresonanz 30 Minuten'),
               ('B60', 'Bioresonanz 60 Minuten'),
               ('B90', 'Bioresonanz 90 Minuten'),
               ('P60', 'Psychotherapie 60 Minuten'),
               ('P90', 'Psychotherapie 90 Minuten'),
               ('E01', 'Erstgespräch')
               )

    x = '12:00'
    
    product= forms.ChoiceField(required=False, widget=forms.widgets.Select(attrs={"placeholder":"Produkt", "class": "form-control"}), label="", choices=PRODUKT)
    note = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Notiz", "class": "form-control"}), label="")
    customer = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Tssext", "class": "form-control"}), label="")
    day = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),initial=datetime.now(), label="")
    time_begin = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'value': '10:00'  }, format='%H:%M'),label="")
    time_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'value': x}),label="")
    text = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")
    googlecalendar = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")
    invoice = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")
   

    class Meta:
        model = Date
        exclude =('user',)

class AddCalenderFormText(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder":"Text", "class": "form-control", "rows":"30"}), label="")
    class Meta:
        model = Date
        fields =('text',)


class AddInvoiceForm(forms.ModelForm):

    number = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Notiz", "class": "form-control"}), label="")
    customer = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Tssext", "class": "form-control"}), label="")
    date_begin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),initial=datetime.now(), label="")
    date_end = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),initial=datetime.now(), label="")
    product= forms.ChoiceField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Produkt", "class": "form-control"}), label="")
    text = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")
    price = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Text", "class": "form-control"}), label="")
    already_paid = forms.BooleanField(required=False, widget=forms.widgets.CheckboxInput(attrs={"placeholder":"Text", "class": "form-check-input"}), label="")
    show_diagnose = forms.BooleanField(required=False, widget=forms.widgets.CheckboxInput(attrs={"placeholder":"Text", "class": "form-check-input"}), label="")
    class Meta:
        model = Invoice
        fields =('date_begin','date_end', 'already_paid', 'show_diagnose')

class AddInvoiceFormRecipent(forms.ModelForm):
    number = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Rechnungsnummer", "class": "form-control"}), label="")
    customer  = forms.ModelChoiceField(required=False,queryset=Customer.objects.all(), widget=forms.widgets.HiddenInput(attrs={"placeholder":"Tssext", "class": "form-control"}), label="")
    reci_title = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Titel", "class": "form-control"}), label="")
    reci_first_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Vorname", "class": "form-control"}), label="")
    reci_last_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Nachname", "class": "form-control"}), label="")
    reci_street =forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Straße", "class": "form-control"}), label="")
    reci_housenumber = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Hausnummer", "class": "form-control"}), label="")
    reci_plz = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"PLZ", "class": "form-control"}), label="")
    reci_city = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Ort", "class": "form-control"}), label="")
    reci_country = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Land", "class": "form-control"}), label="")
    
    class Meta:
        model = Invoice
        exclude =('date_end', 'date_begin', 'product', 'price', 'text','show_diagnose', 'status', 'already_paid')


class AddInvoiceTextForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder":"Text", "class": "form-control", "rows":"3"}), label="")
    class Meta:
        model = Invoice
        fields =('text',)

class AddProductForm(forms.ModelForm):
    number = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Titel", "class": "form-control"}), label="")
    description = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Titel", "class": "form-control"}), label="")
    price = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Titel", "class": "form-control"}), label="")
    count = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Titel", "class": "form-control"}), label="")
    endprice = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={"placeholder":"Rechnungsnummer", "class": "form-control"}), label="")
    factor = forms.DecimalField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Titel", "class": "form-control"}),  step_size=0.1,label="")
    date  = forms.ModelChoiceField(queryset=Date.objects.all(), widget=forms.widgets.HiddenInput(attrs={"placeholder":"Titel", "class": "form-control"}), label="")

    class Meta:
        model = Position
        exclude =('user',)