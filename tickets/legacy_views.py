from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from celery.result import AsyncResult

from .models import Guest, GuestNameChange

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
        "tickets": tickets,
        'hidereturn': True,
        'pending_nc': GuestNameChange.has_pending_namechange(request.user),
        'total_nc_cost': GuestNameChange.namechange_total_cost(request.user)
    }

    ctx.update(common_context)

    return render(request, 'original/ticket_details.tpl', context=ctx) 

@login_required
def user(request):
    return render(request, 'original/user.tpl')

def faq(request):
    ctx = {
        'page_name': 'Frequently Asked Questions'
    }

    ctx.update(common_context)

    return render(request, 'original/faq.tpl', context=ctx)

@staff_member_required(login_url=None)
def admin(request):
    return render(request, 'original/admin.tpl', context=common_context)

def terms(request):
    return render(request, 'original/terms.tpl', context=common_context)

def extract_nc(post_data, i):
    names = ['tid', 'change', 'fname', 'lname']
    out = {}

    for name in names:
        key = 'g%d_%s' % (i, name)
        if key not in post_data:
            return None

        out[name] = post_data[key]

    if len(out) != len(names):
        return None

    return out

@staff_member_required
def ticket_pdf(request):
    if 'jid' not in request.GET:
        raise Http404()
    
    jid = request.GET['jid']

    result = AsyncResult(jid)
    
    return HttpResponse(result.state())

@login_required
def namechange(request):
    if request.method == 'POST':
        count = int(request.POST['g_count'])

        for i in range(count):
            details = extract_nc(request.POST, i)

            if details is None or not details['change']:
                continue

            # create name change for the user
            # check that the user is the owner of this ticket
            ticket = Guest.objects.get(id=details['tid'])

            # print(ticket.owner.id, details.id)
            if ticket.owner != request.user:
                # hack hack hack
                continue

            ticket.create_namechange(details['fname'], details['lname'])

        return redirect('tickets')
    else:
        tickets = Guest.objects.filter(owner=request.user).order_by('id')
        guests = tickets.exclude(parent__isnull=True)

        ctx = {
            "guests": guests
        }

        ctx.update(common_context)

        return render(request, 'original/name_change_request.tpl', context=ctx)
