import datetime
import os.path
import pytz
import oauth2_provider

# Write this code in calendar_app/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from oauth2_provider.views.generic import ProtectedResourceView
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import date, datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, Date, Invoice, Position, PositionDefinition, Anamnese, ProductDefinition
from .forms import AddCustomerForm, AddCalenderForm, AddCalenderFormText, AddInvoiceForm, UpdateAnamneseForm, AddInvoiceFormRecipent, AddProductForm, AddCustomerDiagnoseForm, AddInvoiceTextForm, AddAnamneseForm

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Du wurstest erfolgreich eingeloggt.')
            return redirect(home)
        else:
            messages.success(request, 'Falsches Benutzername oder Passwort')
            return redirect(home)
    else:  
        return render(request, 'home.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, 'Du wurdest erfolgreich ausgeloggt')        
    return redirect(home)

def calendar(request):
    if request.user.is_authenticated:
        return render(request, 'calendar.html', {})
    else:
	    return redirect (home)


def customers(request):
    if request.user.is_authenticated:
        customers = Customer.objects.all().order_by('-id')
        return render(request, 'customers.html', {'customers':customers})
    else:
	    return redirect (home)

def search_customers(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            searched = request.POST['searched']
            customers = Customer.objects.filter(last_name__contains=searched).order_by('-id') | Customer.objects.filter(first_name__contains=searched).order_by('-id')
            return render(request, 'customers.html', {'searched':searched, 'customers': customers})
    else:
	    return redirect (home)

def invoices_open(request):
    if request.user.is_authenticated:

        invoices = Invoice.objects.filter(status='offen').order_by('-date_begin')

        return render(request, 'invoices_open.html', {'invoices':invoices})
    else:
	    return redirect (home)
    
def invoices_canceled(request):
    if request.user.is_authenticated:

        invoices = Invoice.objects.filter(status='storniert').order_by('-date_begin')

        return render(request, 'invoices_canceled.html', {'invoices':invoices})
    else:
	    return redirect (home)
    
def invoices_done(request):
    if request.user.is_authenticated:

        invoices = Invoice.objects.filter(status='bezahlt').order_by('-date_begin')

        return render(request, 'invoices_done.html', {'invoices':invoices})
    else:
        return redirect (home)
    
def invoices_all(request):
    if request.user.is_authenticated:

        invoices = Invoice.objects.all().order_by('-date_begin')

        return render(request, 'invoices_all.html', {'invoices':invoices})
    else:
        return redirect (home)
    
def search_invoice(request, pk):
    if request.user.is_authenticated:



        if request.method == "POST":
            searched = request.POST['searched']
            print(searched)

            if pk == 'all':
                invoices = Invoice.objects.filter(number__contains=searched ).order_by('-date_begin') | Invoice.objects.filter(customer__last_name__contains=searched).order_by('-date_begin') | Invoice.objects.filter(customer__first_name__contains=searched).order_by('-date_begin') 
            else:
                invoices = Invoice.objects.filter(number__contains=searched , status__contains=pk).order_by('-date_begin') | Invoice.objects.filter(customer__last_name__contains=searched, status__contains=pk).order_by('-date_begin') | Invoice.objects.filter(customer__first_name__contains=searched, status__contains=pk).order_by('-date_begin')
            
            if pk == 'offen':
                 pk = 'open'
            elif pk == 'storniert':
                 pk = 'canceled'
            elif pk == 'bezahlt':
                 pk = 'done'
            else:
                 pk = 'all'

            template = 'invoices_' + str(pk) +'.html'
            return render(request, template, {'searched':searched, 'invoices': invoices})
    else:
	    return redirect (home)

def customer(request, pk):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=pk)
        return render(request, 'customer.html', {'customer':customer})
    else:
	    return redirect (home)

def customer_calendar(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        current_calendars = Date.objects.all()
        current_calendars = Date.objects.filter(customer=pk).order_by('-day')

        return render(request, 'customer_calendar.html', {'customer_calendar':current_customer, 'current_calendars':current_calendars})
    else:
	    return redirect (home)

def add_customer(request):
    if request.user.is_authenticated:
        form = AddCustomerForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, "Patient angelegt")
                return redirect(customers) 
        return render(request, 'add_customer.html', {'form': form})
    else:
	    return redirect (home)
       
def delete_customer(request, pk):
    if request.user.is_authenticated:
        delete_it = Customer.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Patiendendaten gelöscht")
        return redirect('customers')
    else:
	    return redirect (home)


def update_customer(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None, instance=current_customer) 
        if form.is_valid():
            form.save()
            messages.success(request, "Patiendendaten geändert")
            return redirect('customer', pk)  
        return render(request, 'update_customer.html', {'form':form,'current_customer':current_customer})
    else:
	    return redirect (home)

def customer_claims(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        current_calendars = Date.objects.all()
        
        current_calendars = Date.objects.filter(customer=pk).order_by('-day')
        count = current_calendars.count()

        print(current_calendars)

        for calendar in current_calendars:
            
            print(calendar.get_product_display())


        return render(request, 'customer_claims.html', {'current_customer':current_customer, "current_calendars": current_calendars, "count": count})
    else:
	    return redirect (home)


def update_calendar(request, pk):
    if request.user.is_authenticated:
        # Authenticate with Google Calendar API
        creds = Credentials.from_authorized_user_file(
            'token.json')  # Path to your token file
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Build Google Calendar API service
        service = build('calendar', 'v3', credentials=creds)
        
        current_calendar= Date.objects.get(id=pk)
        googlecalendar = current_calendar.googlecalendar

        customer.id = current_calendar.customer
        current_customer= Customer.objects.get(id=customer.id)
        form = AddCalenderForm(request.POST or None, instance=current_calendar) 
        if form.is_valid():
            form.save()
            messages.success(request, "Termin geändert")

            event = service.events().get(calendarId='r71pa4c167gc1vqs42u57vdshc@group.calendar.google.com', eventId=googlecalendar).execute()

            summary= f"{current_customer.last_name}, {current_customer.first_name}"
            begin = f"{form.cleaned_data["day"] }T{form.cleaned_data["time_begin"]}+02:00:00"
            end = f"{form.cleaned_data["day"] }T{form.cleaned_data["time_end"]}+02:00:00"
            note = f"{form.cleaned_data["note"]}"
            product = f"{form.cleaned_data["product"]} "
            description = (f"{product} Minuten\n"
                            f"{note}"
                            )
        

            if product[0] == "B":
                colorId = 1
            else:
                colorId = 2

            mail = current_customer.mail
            if mail == '':
                mail = "support@eumelpraxis.de"
            

            event = {
            'summary':  summary,
            'location': 'Eumelpraxis',
            'description': description,
            'start': {
                'dateTime': begin,
                    'timeZone': 'Europe/Berlin',
            },
            'end': {
                'dateTime': end,
                    'timeZone': 'Europe/Berlin',
            },

            'attendees': [
                {'email': mail},
            ],

            'colorId': colorId,             

            }

            service.events().update(calendarId='r71pa4c167gc1vqs42u57vdshc@group.calendar.google.com', eventId=googlecalendar, body=event).execute()

            return redirect('customer_calendar', customer.id)  
        return render(request, 'update_calendar.html', {'form':form,'current_calendar':current_calendar, "current_customer": current_customer})
    else:
	    return redirect (home)
    
def edit_calendar_text(request, pk):
    if request.user.is_authenticated:
        current_calendar= Date.objects.get(id=pk)
        customer.id = current_calendar.customer
        current_customer= Customer.objects.get(id=customer.id)
        form = AddCalenderFormText(request.POST or None, instance=current_calendar) 
        if form.is_valid():
            form.save()
            messages.success(request, "Text gespeichert")
            return redirect( 'calendar_detail', pk)
        return render(request, 'edit_calendar_text.html', {'form':form,'current_calendar':current_calendar, "current_customer": current_customer})
    else:
	    return redirect (home)

def delete_calendar(request, pk):
    if request.user.is_authenticated:
        # Authenticate with Google Calendar API
        creds = Credentials.from_authorized_user_file(
            'token.json')  # Path to your token file
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Build Google Calendar API service
        service = build('calendar', 'v3', credentials=creds)

        delete_it = Date.objects.get(id=pk)

        positions = Position.objects.filter(date=delete_it)
        for position in positions:
            position.delete()
        customer.id = delete_it.customer
        googlecalendar = delete_it.googlecalendar
        service.events().delete(calendarId='r71pa4c167gc1vqs42u57vdshc@group.calendar.google.com', eventId=googlecalendar).execute()
        delete_it.delete()
        messages.success(request, "Termin gelöscht")
        return redirect( 'customer_calendar', customer.id)
    else:
	    return redirect (home)
    
def calendar_detail(request,pk):
    if request.user.is_authenticated:
        current_calendar = Date.objects.get(id=pk)
        current_customer = Customer.objects.get(id=current_calendar.customer)
        return render(request, 'calendar_detail.html', {'current_calendar':current_calendar, 'current_customer': current_customer})
    else:
	    return redirect (home)


# def fetch_events(request):
#     try:
#         # Authenticate with Google Calendar API
#         creds = Credentials.from_authorized_user_file(
#             'token.json')  # Path to your token file
#         if creds.expired and creds.refresh_token:
#             creds.refresh(Request())

#         # Build Google Calendar API service
#         service = build('calendar', 'v3', credentials=creds)

#         # Retrieve events from Google Calendar
#         now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#         events_result = service.events().list(
#             calendarId='r71pa4c167gc1vqs42u57vdshc@group.calendar.google.com', timeMin=now,  singleEvents=True,
#             orderBy='startTime').execute()
#         events_data = events_result.get('items', [])

#         # Save events to the database
#         for event_data in events_data:
#             start_time = event_data['start'].get(
#                 'dateTime', event_data['start'].get('date'))
#             end_time = event_data['end'].get(
#                 'dateTime', event_data['end'].get('date'))
#             start_time = datetime.datetime.fromisoformat(start_time)
#             end_time = datetime.datetime.fromisoformat(end_time)

#             # Save event to the database
#             Event.objects.create(
#                 summary=event_data.get('summary', ''),
#                 start_time=start_time,
#                 end_time=end_time
#             )

#         # Retrieve events from the database and display
#         events = Event.objects.all()
#         context = {'events': events}
#         return render(request, 'calendar.html', context)

#     except Exception as e:
#         return HttpResponse(f"An error occurred: {e}")


def add_calendar(request, pk):
    if request.user.is_authenticated:
        # Authenticate with Google Calendar API
        creds = Credentials.from_authorized_user_file(
            'token.json')  # Path to your token file
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Build Google Calendar API service
        service = build('calendar', 'v3', credentials=creds)

        current_customer = Customer.objects.get(id=pk)
        form = AddCalenderForm(request.POST or None )

        
        if request.method == "POST":
                
                if form.is_valid():
                    # add_calendar = form.save()
                    messages.success(request, "Termin angelegt")
                    
                    summary= f"{form.cleaned_data["product"]} {current_customer.last_name}, {current_customer.first_name}"
                    begin = f"{form.cleaned_data["day"] }T{form.cleaned_data["time_begin"]}+02:00:00"
                    end = f"{form.cleaned_data["day"] }T{form.cleaned_data["time_end"]}+02:00:00"
                    note = f"{form.cleaned_data["note"]}"
                    product = f"{form.cleaned_data["product"]} "
                    description = (f"{product} Minuten\n"
                                f"{note}"
                                )
                    
                
                    if product[0] == 'B':
                        colorId = 1

                    else:
                        colorId = 2
    

                    mail = current_customer.mail
                    if mail == '':
                        mail = "support@eumelpraxis.de"
                

                    event = {
                    'summary':  summary,
                    'location': 'Eumelpraxis',
                    'description': description,
                    'start': {
                        'dateTime': begin,
                        'timeZone': 'Europe/Berlin',
                    },
                    'end': {
                        'dateTime': end,
                        'timeZone': 'Europe/Berlin',
                    },

                    'attendees': [
                        {'email': mail},
                    ],

                    'colorId': colorId,             

                    }

                    event = service.events().insert(calendarId='r71pa4c167gc1vqs42u57vdshc@group.calendar.google.com', body=event).execute()
                    # eventid = '9b8dc7qls8o6fpm3a9lt5f8r54'
                    eventid = event.get('id')
                    form.save()
                    
                    current_date = Date.objects.latest('id')
                    current_date.googlecalendar = eventid
                    current_date.save()

                    
                    #position.save()

                return redirect(create_positions,current_date.id)
    
        form = AddCalenderForm(initial={'customer': pk})

        return render(request, 'add_calender.html', {'form': form, 'current_customer': current_customer})
    else:
	    return redirect (home)

def create_positions(request, pk):
    if request.user.is_authenticated:
        current_date = Date.objects.get(id=pk)
        current_customer = Customer.objects.get(id=current_date.customer)
        positions = PositionDefinition.objects.filter(product=current_date.product)

        for position in positions:
             add_position = Position.objects.create(number=position.number,description=position.description,count=position.count,factor=position.factor,date=current_date, price=position.price)

        return redirect(customer_calendar,current_customer.id)
    else:
	    return redirect (home)


def add_invoice (request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        today = date.today()
        timestamp = today.strftime("%y%d%m")

        invoice_unique = False
        x = 1
        
        while invoice_unique == False:
            current_invoice = 'RG-' + str(current_customer.id) + '-' + timestamp + '-' + str(x) 

            invoices = Invoice.objects.filter(number__contains=current_invoice)

            if invoices.exists():
                x = x + 1 

            else:
                invoice_unique = True
    
        current_invoice = 'RG-' + str(current_customer.id) + '-' + timestamp + '-' + str(x) 
        form = AddInvoiceFormRecipent(request.POST or None, initial={ 'reci_title': current_customer.title,
                                        'reci_first_name': current_customer.first_name,
                                        'reci_last_name': current_customer.last_name,
                                        'reci_street': current_customer.street,
                                        'reci_housenumber': current_customer.housenumber,
                                        'reci_plz': current_customer.plz,
                                        'reci_city': current_customer.city,
                                        'reci_country': current_customer.country,
                                        'number': current_invoice,
                                        'customer': current_customer})  


        if request.method == "POST":
            if form.is_valid():
                form.save()
                #messages.success(request, "Rechnung angelegt")
                return redirect(add_invoice2, current_invoice) 
        return render(request, 'add_invoice.html', {'form': form,'current_customer':current_customer})
    else:
	    return redirect (home)

def customer_invoice(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        customer_invoices = Invoice.objects.filter(customer=pk).order_by('-id') 
        return render(request, 'customer_invoice.html', {'current_customer':current_customer, 'customer_invoices': customer_invoices})
    else:
	    return redirect (home)


def add_invoice2(request, pk):
    if request.user.is_authenticated:
  
        customer_invoices =  Invoice.objects.get(number=pk)
        current_customer = customer_invoices.customer
        current_calendars = Date.objects.filter(customer=current_customer.id, invoice = '').order_by('-day')

        form = AddInvoiceFormRecipent(request.POST or None)
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')

            for x in id_list:
                Date.objects.filter(pk=int(x)).update(invoice=pk)

            print(id_list)
            if not id_list:
                customer_invoices.delete()
                return redirect(home)
            else:
                print()

            return redirect(add_invoice3, customer_invoices.id) 

        return render(request, 'add_invoice_2.html', {'form': form, 'current_calendars': current_calendars})
    else:
	    return redirect (home)
    
def invoice_detail(request, pk):
    if request.user.is_authenticated:
        current_invoice = Invoice.objects.get(id=pk)
        current_customer = current_invoice.customer

    
        calendars = Date.objects.filter(invoice=current_invoice.number)

        list = []
        sum = 0


        for calendar in calendars:
            positions = Position.objects.filter(date=calendar)
            termin = 'Termin vom: ' + str(calendar.day.strftime("%d.%m.%y"))

            list_positions = []
            list.append([termin])
            for position in positions:
                list_positions = []
                list_positions.append(position.number)
                list_positions.append(position.description)
                list_positions.append(position.count)
                list_positions.append(position.factor)
                list_positions.append(position.price)
                list_positions.append(position.endprice2)
                
                sum = sum + position.endprice2

                list.append(list_positions)

        
        Invoice.objects.filter(id=pk).update(price=sum)
        print(current_invoice.price)

        return render(request, 'invoice_detail.html',{'current_customer':current_customer, 'current_invoice': current_invoice,'calendars': calendars, 'list':list, 'sum':sum})
    else:
	    return redirect (home)

def positions(request, pk):
    if request.user.is_authenticated:
        current_calendar = Date.objects.get(id=pk)
        current_customer = Customer.objects.get(id=current_calendar.customer)
        current_positions = Position.objects.filter(date=pk)
        summe = 0
        for x in current_positions:
            summe = summe + x.endprice2
        return render(request, 'positions.html', {'current_customer':current_customer, 'current_calendar': current_calendar, 'current_positions': current_positions, 'summe':summe})
    else:
	    return redirect (home)
    
def position_detail(request,pk):
    if request.user.is_authenticated:
        current_positions = Position.objects.get(id=pk)
        current_calendar =  current_positions.date
        current_customer = Customer.objects.get(id=current_calendar.customer)
        form = AddProductForm(request.POST or None, instance=current_positions) 
        if form.is_valid():
            form.save()
            messages.success(request, "Gebührenpositionen geändert")
            return redirect('positions', current_positions.date.id)  

        return render(request, 'position_detail.html', {'form':form,'current_customer':current_customer,'current_positions': current_positions,  'current_calendar': current_calendar})
    else:
	    return redirect (home)

def delete_invoice(request, pk):
    if request.user.is_authenticated:
        delete_it = Invoice.objects.get(id=pk)

        print(delete_it)
        current_customer = delete_it.customer
        
        calendars = Date.objects.filter(invoice=delete_it.number)
        for calendar in calendars:
            calendars = Date.objects.filter(invoice=delete_it.number).update(invoice='')
            
        delete_it.delete()
        messages.success(request, "Rechnung gelöscht")
        return redirect('customer_invoice',current_customer.id)
    else:
	    return redirect (home)
    
def update_invoice_reci (request, pk):
    if request.user.is_authenticated:
        current_invoice = Invoice.objects.get(id=pk)
        form = AddInvoiceFormRecipent(request.POST or None, instance=current_invoice) 
        if form.is_valid():
            form.save()
            messages.success(request, "Empfänger geändert")
            return redirect('invoice_detail', pk)  
        return render(request, 'update_invoice_reci.html', {'form':form,'current_invoice':current_invoice})
    else:
	    return redirect (home)

def add_invoice3 (request, pk):
    if request.user.is_authenticated:
        current_invoice = Invoice.objects.get(id=pk)
        current_dateTime = datetime.now()

        form = AddInvoiceForm(request.POST or None, instance=current_invoice, initial={'date_begin': current_dateTime,
                                                                          'date_end' : current_dateTime+ timedelta(days=14)})

        if form.is_valid():
            form.save()
            messages.success(request, "Rechnung angelegt")
            print(current_invoice.already_paid)
            if current_invoice.already_paid == True:
                Invoice.objects.filter(id=pk).update(status='bezahlt')

            return redirect('invoice_detail', pk)  
        return render(request, 'add_invoice_3.html', {'form':form,'current_invoice':current_invoice})
    else:
	    return redirect (home)
    
def update_invoice_date (request, pk):
    if request.user.is_authenticated:
        current_invoice = Invoice.objects.get(id=pk)
    
        form = AddInvoiceForm(request.POST or None, instance=current_invoice)

        if form.is_valid():
            form.save()
            if current_invoice.already_paid == True:
                Invoice.objects.filter(id=pk).update(status='bezahlt')
            else:
                Invoice.objects.filter(id=pk).update(status='offen')

            messages.success(request, "Datum geändert")
            return redirect('invoice_detail', pk)  
        return render(request, 'add_invoice_3.html', {'form':form,'current_invoice':current_invoice})
    else:
	    return redirect (home)
    
def customer_diagnose(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        form = AddCustomerDiagnoseForm(request.POST or None,instance=current_customer)

        if form.is_valid():
            form.save()
            messages.success(request, "Diagnose geändert")
            return redirect(customer, pk)  

        return render(request, 'customer_diagnose.html', {'form':form, 'current_customer': current_customer})  
    else:
	    return redirect (home)
    
def update_invoice_text(request, pk):
    if request.user.is_authenticated:
        current_invoice = Invoice.objects.get(id=pk)
        form = AddInvoiceTextForm(request.POST or None,instance=current_invoice)

        if form.is_valid():
            form.save()
            messages.success(request, "Text geändert")
            return redirect(invoice_detail, pk)  

        return render(request, 'update_invoice_text.html', {'form':form, 'current_invoice': current_invoice})   
    else:
	    return redirect (home)
    
def accept_invoice(request, pk):
    if request.user.is_authenticated:
        Invoice.objects.filter(id=pk).update(status='bezahlt')
        messages.success(request,"Rechnung freigegeben")
        return redirect(invoice_detail,pk)
    else:
	    return redirect (home)  

def storno_invoice(request, pk):
    if request.user.is_authenticated:
        Invoice.objects.filter(id=pk).update(status='storniert')
        messages.success(request,"Rechnung storniert")
        return redirect(invoice_detail,pk)
    else:
	    return redirect (home)  

def anamnese(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        anamneses = Anamnese.objects.filter(customer=current_customer)
   
        return render(request, 'anamnese.html', {'anamneses': anamneses, 'current_customer': current_customer})   
    else:
	    return redirect (home)
    
def add_anamnese(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)

        form = AddAnamneseForm(request.POST or None, initial={'customer': current_customer})
        print(current_customer)

        if request.method == "POST":
            if form.is_valid():
                
                form.save()
                messages.success(request, "Anamnese angelegt")
                return redirect('anamnese', current_customer.id)  

        return render(request, 'add_anamnese.html', {'form':form, 'current_customer': current_customer})   
    else:
	    return redirect (home)
    
def update_anamnese(request, pk):
    if request.user.is_authenticated:
        current_anamnese = Anamnese.objects.get(id=pk)
        current_customer = current_anamnese.customer
        form = UpdateAnamneseForm(request.POST or None,instance=current_anamnese)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Anamnese geändert")
                return redirect(anamnese, current_customer.id)  

        return render(request, 'update_anamnese.html', {'form':form, 'current_anamnese': current_anamnese, 'current_customer': current_customer})   
    else:
	    return redirect (home)
    
