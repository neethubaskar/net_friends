from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from user_profile.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates that the email is unique, passwords match, and the password
    meets the required criteria.
    """
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    date_of_birth = serializers.DateField(
        input_formats=["%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y"], required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'date_of_birth')

    def validate_email(self, value):
        """
        Check that the email is unique.
        :param value: The email to validate.
        :return: The validated email.
        :raises serializers.ValidationError: If the email is already in use.
        """
        if UserProfile.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                "A user with that email already exists.")
        return value

    def validate(self, attrs):
        """
        Check that the two password fields match.
        :param attrs: The validated data.
        :return: The validated data.
        :raises serializers.ValidationError: If the passwords do not match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        :param validated_data: The data validated by the serializer.
        :return: The newly created user.
        """
        validated_data.pop('password2')
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates that the credentials are entered correctly for login.
    """
    email = serializers.EmailField(
        required=True, max_length=254,
        error_messages={'required': 'Please enter valid email address',
                        'blank': 'Please enter valid email address.'}
    )
    password = serializers.CharField(
        required=True, max_length=128,
        error_messages={'required': 'Please enter password',
                        'blank': 'Please enter password.'}
    )

    def validate_email(self, value):
        """
        Converting email from request data to lowercase.
        The email to validate.
        :return: The validated email.
        """
        value = value.lower()
        return value


class UserSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for searching users by email or name.
    """
    date_joined = serializers.DateTimeField(
        format='%d/%m/%Y %H:%M:%S', required=False, allow_null=True)
    date_of_birth = serializers.DateField(
        format='%d/%m/%Y', required=False, allow_null=True)
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'date_of_birth', 
                  'date_joined', 'followers_count', 'request_count')
