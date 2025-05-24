from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with validation.
    """
    email = serializers.EmailField(
        required=True,
        help_text="User's email address"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="User's password (min 8 characters)"
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm password (must match password)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'username': {
                'required': True,
                'help_text': "User's unique username"
            }
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

#Wisua: This serializer is used for user login, it validates the username and password, and generates a JWT token upon successful authentication.
#You can read about JWT tokens here: https://www.django-rest-framework.org/api-guide/authentication/#json-web-token-authentication
class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField(
        required=True,
        help_text="User's unique username"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="User's password"
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        """
        Validate the login credentials.
        """
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username does not exist.")

        user = User.objects.get(username=username)

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        # Add the user to the validated data so we can access it in get_token
        data['user'] = user
        return data

    def get_token(self):
        """
        Generate JWT token for the authenticated user.
        """
        user = self.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }