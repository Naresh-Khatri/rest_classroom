from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"

class CalenderEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalenderEvent
        fields = '__all__'


class MeetingSerializer(serializers.ModelSerializer):
    creater_name = serializers.SerializerMethodField(source='get_creater_name')
    instructor_name = serializers.SerializerMethodField(source='get_instructor_name')
    class Meta:
        model = models.Meeting
        fields = ["id","date","starting_at","ending_at","subject","topic","link", "instructor", "creater", "instructor_name" , 'creater_name']
    def get_creater_name(self, obj):
        return obj.creater.username

    def get_instructor_name(self, obj):
        return obj.instructor.username