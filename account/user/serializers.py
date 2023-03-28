from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, UserToken, UserQuestion
from django.http import HttpResponse


class UserRegisterSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(max_length=100, required=True)
    lastname = serializers.CharField(max_length=100, required=True)
    birthdate = serializers.DateField(required=True)
    nationality = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=100, required=True)
    re_password = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'birthdate', 'nationality', 'email', 'password', 're_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            birthdate=validated_data['birthdate'],
            nationality=validated_data['nationality'],
            email=validated_data['email'],
            password=validated_data['password'],
            re_password=validated_data['re_password']
        )
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserForgetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=100)

    class Meta:
        model = UserToken
        fields = ['token']


class UserResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, required=True)
    re_password = serializers.CharField(max_length=100, required=True)
    token = TokenSerializer()
    timeout = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['password', 're_password', 'token', 'timeout']

    def validate(self, attrs):
        token = attrs['token']['token']
        if not UserToken.objects.filter(token=token).exists():
            raise serializers.ValidationError(
                {"user": "Sorry user not found."})
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    question = serializers.CharField(max_length=500)
    token = TokenSerializer()

    class Meta:
        model = UserQuestion
        fields = ['question', 'token']

    def validate(self, attrs):
        token = attrs['token']['token']
        if not UserToken.objects.filter(token=token).exists():
            raise serializers.ValidationError(
                {"user": "Sorry user not found."})
        return attrs
