from rest_framework import serializers
from .social_helpers import google, facebook
from .social_helpers.register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
from fitila.settings import GOOGLE_CLIENT_ID


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        if type(user_data) == dict:
            try:
                user_id = user_data['id']
                email = user_data['email']
                name = user_data['name']
                provider = 'facebook'
                return register_social_user(
                    provider=provider,
                    user_id=user_id,
                    email=email,
                    name=name
                )
            except Exception as identifier:
                print(identifier)

                raise serializers.ValidationError(
                    'The token is invalid or expired. Please login again.'
                )
        else:
            raise serializers.ValidationError(user_data)
        


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        
        if user_data['aud'] != GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')


        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)


