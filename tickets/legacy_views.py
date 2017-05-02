from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Guest

common_context = {
    "event_name": "King's Affair 2017",
    "site_name": "Online Ticketing System"
}

@login_required
def tickets(request):
    tickets = Guest.objects.filter(owner=request.user).order_by('id')
    primary = tickets.get(parent__isnull=True)

    ctx = {
        "user": request.user,
        "primary": primary,
        "tickets": tickets
    }

    ctx.update(common_context)

    return render(request, 'original/ticket_details.tpl', context=ctx) 

@login_required
def user(request):
    return render(request, 'original/user.tpl')

def faq(request):
    return render(request, 'original/faq.tpl', context=common_context)

@staff_member_required(login_url=None)
def admin(request):
    return render(request, 'original/admin.tpl', context=common_context)

def terms(request):
    return render(request, 'original/terms.tpl', context=common_context)
