from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route, renderer_classes

from django.contrib.auth.models import User

from .serializers import UserSerializer, GuestSerializer
from .models import Guest
from .tasks import generate_qrcode

from .legacy_views import *

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('fname', 'lname', 'owner__username', 'category')

    @detail_route(methods=['GET'])
    def qr(self, request, pk=None):
        """
        Lazily generate a QR code if one does not exist. If the QR code exists,
        return a URL pointing to it.
        """
        guest = self.get_object()
        result = {}

        if not guest.qr_code:
            # TODO: provide status feedback
            generate_qrcode.delay(guest.id, guest.hash)
            result['status'] = 'generating'
        else:
            result['status'] = 'generated'
            result['url'] = guest.qr_code.url

        return Response(result)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
