from rest_framework import serializers

from django.contrib.auth.models import User, Group

from .models import Guest

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class GuestSerializer(serializers.HyperlinkedModelSerializer):

    # TODO: override create method so that we can asynchronously allocate
    # tickets up to the max count

    class Meta:
        model = Guest
        fields = ('id', 'owner', 'fname', 'lname', 'category', 'reentry_allowed', 'price', 'waiting', 'payment_method', 'parent')
