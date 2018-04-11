from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer

class UserSerializer(UserDetailsSerializer):
    # balance = serializers.JSONField(source="userprofile.balance")
    datasets = serializers.JSONField(source="userprofile.datasets")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            # 'balance',
            'datasets',
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})

        instance = super(UserSerializer, self).update(instance, validated_data)

        # Get and update user profile.
        if profile_data:
            profile = instance.userprofile
            # Do not let users change their balances.
            # balance = profile_data.get('balance')
            # if balance != None:
            #     profile.balance = balance

            datasets = profile_data.get('datasets')
            if datasets != None:
                # Should check here that the user actually changed their dataset.
                profile.datasets = datasets
            profile.save()
        return instance

from rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    # balance = serializers.JSONField(source="userprofile.balance", required=False, write_only=True)
    datasets = serializers.JSONField(source="userprofile.datasets", required=False, write_only=True)

    def get_cleaned_data(self):
        profile_data = self.validated_data.pop('userprofile', {})
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            # 'balance': profile_data.get('balance', {}),
            'datasets': profile_data.get('datasets', {})
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()

        profile = user.userprofile

        # Do not let users set their own balance on registration.
        # balance = self.cleaned_data.get('balance')
        # if balance != None:
        #     profile.balance = balance

        datasets = self.cleaned_data.get('datasets')
        if datasets != None:
            # Should check here that the user actually uploaded this dataset.
            profile.datasets = datasets

        profile.save()
        return user
