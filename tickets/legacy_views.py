from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

common_context = {
	"event_name": "King's Affair 2017",
	"site_name": "Online Ticketing System"
}

@login_required
def tickets(request):
    return render(request, 'original/main.tpl', context={"user": request.user}) 

@login_required
def user(request):
	return render(request, 'original/user.tpl')

def faq(request):
	return render(request, 'original/faq.tpl', context=common_context)

@staff_member_required(login_url=None)
def admin(request):
	return render(request, 'original/admin.tpl', context=common_context)
	