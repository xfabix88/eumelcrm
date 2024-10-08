from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('calendar/', views.calendar, name="calendar"),
    path('customers/', views.customers, name="customers"),
    path('search_customers/', views.search_customers, name="search_customers"),   
    path('invoices_open/', views.invoices_open, name="invoices_open"),
    path('invoices_canceled/', views.invoices_canceled, name="invoices_canceled"),
    path('invoices_done/', views.invoices_done, name="invoices_done"),
    path('invoices_all/', views.invoices_all, name="invoices_all"),
    path('customer/<int:pk>', views.customer, name="customer"),
    path('add_customer/', views.add_customer, name="add_customer"),
    path('delete_customer/<int:pk>', views.delete_customer, name="delete_customer"),
    path('update_customer/<int:pk>', views.update_customer, name="update_customer"),
    path('customer_diagnose/<int:pk>', views.customer_diagnose, name="customer_diagnose"),  
    path('customer_calendar/<int:pk>', views.customer_calendar, name="customer_calendar"),
    path('add_calendar/<int:pk>', views.add_calendar, name="add_calendar"),
    path('update_calendar/<int:pk>', views.update_calendar, name="update_calendar"),
    path('edit_calendar_text/<int:pk>', views.edit_calendar_text, name="edit_calendar_text"),
    path('delete_calendar/<int:pk>', views.delete_calendar, name="delete_calendar"),
    path('calendar_detail/<int:pk>', views.calendar_detail, name="calendar_detail"),
    path('customer_claims/<int:pk>', views.customer_claims, name="customer_claims"),
    # path('calendar/', views.CalendarView.as_view(), name='calendar'),
   #  path('fetch-events/', views.fetch_events, name='fetch_events'),
    path('customer_invoice/<int:pk>', views.customer_invoice, name="customer_invoice"),
    path('add_invoice/<int:pk>', views.add_invoice, name="add_invoice"),
    path('add_invoice2/<str:pk>', views.add_invoice2, name="add_invoice2"),
    path('add_invoice3/<str:pk>', views.add_invoice3, name="add_invoice3"),
    path('delete_invoice/<str:pk>', views.delete_invoice, name="delete_invoice"),
    path('search_invoice/<str:pk>', views.search_invoice, name="search_invoice"),   
    path('positions/<int:pk>', views.positions, name="positions"),
    path('create_positions/<int:pk>', views.create_positions, name="create_positions"),
    path('position_detail/<int:pk>', views.position_detail, name="position_detail"),
    path('invoice_detail/<int:pk>', views.invoice_detail, name="invoice_detail"),
    path('update_invoice_reci/<str:pk>', views.update_invoice_reci, name="update_invoice_reci"),
    path('update_invoice_date/<str:pk>', views.update_invoice_date, name="update_invoice_date"),
    path('update_invoice_text/<str:pk>', views.update_invoice_text, name="update_invoice_text"),
    path('accept_invoice/<str:pk>', views.accept_invoice, name="accept_invoice"),
    path('storno_invoice/<str:pk>', views.storno_invoice, name="storno_invoice"),
    path('anamnese/<int:pk>', views.anamnese, name='anamnese'),
    path('add_anamnese/<int:pk>', views.add_anamnese, name='add_anamnese'),
    path('update_anamnese/<int:pk>', views.update_anamnese, name='update_anamnese')
]
