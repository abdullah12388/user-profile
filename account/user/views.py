from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
# from django.core.mail import send_mail
from .models import User, UserToken, UserQuestion
from .serializers import UserRegisterSerializer, \
    UserLoginSerializer, UserForgetPasswordSerializer, UserResetPasswordSerializer, UserProfileSerializer
from django.conf import settings
from .tasks import send_email_task
from django.core import serializers
from .chatGPT import generate_response
import datetime

# Create your views here.


class Register(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class Login(APIView):
    def post(self, request):
        log_ser = UserLoginSerializer(data=request.data)
        log_ser.is_valid(raise_exception=True)
        email = log_ser.validated_data['email']
        password = log_ser.validated_data['password']
        try:
            user = User.objects.get(email=email)
            if user.password != password:
                return JsonResponse({'password': 'password is wrong'}, status=422)
            token = UserToken.objects.get(user=user)
            data = {
                'user': {
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'birthdate': user.birthdate,
                    'nationality': user.nationality,
                    'email': user.email
                },
                'token': token.token
            }
            return JsonResponse(data, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'user': 'User not found'}, status=404)


class ForgetPassword(APIView):
    def post(self, request):
        fgt_pass_ser = UserForgetPasswordSerializer(data=request.data)
        fgt_pass_ser.is_valid(raise_exception=True)
        email = fgt_pass_ser.validated_data['email']
        try:
            user = User.objects.get(email=email)
            user_token = UserToken.objects.get(user=user)
            subject = 'Forgot Password'
            timeout = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            link = f'http://localhost:4200/reset-password?token={user_token.token}&timeout={timeout}'
            html_message = f"""
            Dear {user.firstname},
            
            We sending you this Link for resetting your password.
            You can reset now via:
            
            {link}
            
            Make sure to create a strong password and memorize it well.
            
            *Note this link will EXPIRED after 15 minutes.
            
            Best regards,
            Website Team
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_email_task.delay(subject, html_message, from_email, recipient_list)
            data = {
                'user': 'Reset Password E-mail sent successfully'
            }
            return JsonResponse(data, status=200)
        except ObjectDoesNotExist:
            data = {
                'error': 'User not found'
            }
            return JsonResponse(data)


class ResetPassword(APIView):
    def post(self, request):
        rst_pass_ser = UserResetPasswordSerializer(data=request.data)
        rst_pass_ser.is_valid(raise_exception=True)
        timenow = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        timeout = rst_pass_ser.validated_data['timeout']
        if (timenow-timeout) < 1500:
            password = rst_pass_ser.validated_data['password']
            re_password = rst_pass_ser.validated_data['re_password']
            token = rst_pass_ser.validated_data['token']['token']
            user_token = UserToken.objects.get(token=token).user
            user = User.objects.get(firstname=user_token.firstname)
            user.password = password
            user.re_password = re_password
            user.save()
            data = {
                'user': 'password updated successfully'
            }
            return JsonResponse(data, safe=False)
        else:
            data = {
                'expired': 'Reset Password Link Expired'
            }
            return JsonResponse(data, safe=False)


class UserProfile(APIView):
    def get(self, request):
        token = request.GET.get('token', '')
        try:
            user = UserToken.objects.get(token=token).user
            questions = UserQuestion.objects.filter(user=user)
            question_list = []
            for q in questions:
                question_list.append({
                    'question': q.question,
                    'answer': q.answer
                })
            data = {
                'history': question_list
            }
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'user': 'user not found'}, safe=False)

    def post(self, request):
        user_profile_serializer = UserProfileSerializer(data=request.data)
        user_profile_serializer.is_valid(raise_exception=True)
        token = user_profile_serializer.validated_data['token']
        question = user_profile_serializer.validated_data['question']
        answer = generate_response(question)
        # print(question)
        # print(token['token'])
        # print(answer)
        user = UserToken.objects.get(token=token['token'])
        # print(user.user)
        UserQuestion.objects.create(
            user=user.user,
            question=question,
            answer=answer
        )
        data = {
            # 'question': question,
            'answer': answer,
        }
        return JsonResponse(data, safe=False)

