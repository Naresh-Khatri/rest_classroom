from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import datetime
from . import serializers
from . import models
from django.contrib.auth.models import User
from dj_rest_auth.views import LoginView


class CustomLoginView(LoginView):
    '''To send is_staff in response'''
    def get_response(self):
        orginal_response = super().get_response()
        user = self.request.user
        mydata = {"is_staff": user.is_staff}
        orginal_response.data.update(mydata)
        return orginal_response


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer


class CalenderEventsViewSet(viewsets.ModelViewSet):
    queryset = models.CalenderEvent.objects.all()
    serializer_class = serializers.CalenderEventsSerializer

    def perform_create(self, serializer):
        serializer.save(creater = self.request.user)
        

class MeetingsViewSet(viewsets.ModelViewSet):
    queryset = models.Meeting.objects.order_by('starting_at')
    serializer_class = serializers.MeetingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_fields = ['date']

    def perform_create(self, serializer):
        serializer.save(creater = self.request.user)
