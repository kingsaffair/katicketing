from rest_framework import viewsets, filters
from django.contrib.auth.models import User

from .serializers import UserSerializer, GuestSerializer
from .models import Guest

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('fname', 'lname', 'owner__username', 'category')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
