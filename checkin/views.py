from datetime import datetime

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required

from tickets.models import Guest

global_context = {
    'event_name': 'King\'s Affair 2017'
}

@staff_member_required
def checkin(request, hash=None):
    ctx = {
        'mode': request.session.get('checkin_mode', None)
    }
    ctx.update(global_context)
    
    if request.method == 'POST':
        # eww
        ticket_ids = [int(t[2:]) for t in request.POST if t.startswith('t_') and request.POST[t] == '1']
        
        if ctx['mode'] == 'checkin':
            Guest.objects.filter(id__in=ticket_ids).update(checked_in=datetime.now()) 
        elif ctx['mode'] == 'collect':
            Guest.objects.filter(id__in=ticket_ids).update(collected=datetime.now())

    if hash is None:
        return render(request,'old_checkin/ticket-general.tpl', global_context)

    ticket = Guest.objects.get(code=hash)
    tickets = Guest.objects.filter(owner=ticket.owner)

    ctx.update({
        'hash': hash,
        'ticket': ticket,
        'tickets': tickets,
    })

    if ctx['mode'] == 'checkin':
        return render(request,'old_checkin/ticket-entry.tpl', ctx)
    elif ctx['mode'] == 'collect':
        return render(request,'old_checkin/ticket-collection.tpl', ctx)        
    else:
        return render(request,'old_checkin/ticket-basic.tpl', ctx)        

@staff_member_required
def set_mode(request, mode='checkin'):
    request.session['checkin_mode'] = mode
    return redirect('check-in')
