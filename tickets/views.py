import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db import transaction

from .models import Ticket
from .forms import TicketFormSet

@login_required
def ticket_buying_status(request):
    pass


MAX_TICKET_COUNT = 1600

@login_required
def buy_ticket(request):
    if request.method == 'POST':
        # 2. put it on the queue to be processed
        # process_ticket.apply_async(args=ticket_objects)

        # res = HttpResponse()
        # res.status_code = 202 # in progress
        # res['Location'] = reverse('tickets-ticket-buying-status')

        tickets = TicketFormSet(request.POST)

        print(tickets)

        # primary = TicketForm(request.POST)

        # if not primary.is_valid():
        #     return HttpResponseBadRequest()

        # primary = primary.save(commit=False)
        # primary.owner = request.user


        # new_tickets = [primary]

        # # TODO: use asynchronous processing once we've profiled this.
        # with transaction.atomic():
        #     tickets = Ticket.objects.filter(waiting=False).count()

        #     available_tickets = MAX_TICKET_COUNT - tickets

        #     # allocate tickets as available
        #     for t in new_tickets:
        #         if available_tickets >= 1:
        #             t.waiting = False
        #         else:
        #             t.waiting = True

        #         t.save()
        #         available_tickets -= 1

        return render(request, 'form.html', {'form': ''})
    else:
        form = TicketFormSet()
        return render(request, 'form.html', {'form': form.as_p() })
