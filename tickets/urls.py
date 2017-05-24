from django.conf.urls import url, include

from .views import *

urlpatterns = [
	url('user', user, name='user'),
	url('logout', user, name='user-logout'),
	url('faq', faq, name='faq'),
	url('admin', admin, name='ticket-admin'),
    url('ticket_pdf', ticket_pdf, name='ticket-pdf'),
	url('terms', terms, name='terms'),
	url('namechange', namechange, name='namechange'),
	url('', tickets, name='tickets'),
]
