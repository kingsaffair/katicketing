from django.shortcuts import render

# Create your views here.
def night_view(request):
    return render(request, 'night.html') 

