# views.py
from typing import Any
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TokenSerializer
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .utils import VerifyCodeGenerator
import requests

class BaseResetPassword(GenericAPIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.code_generator = VerifyCodeGenerator()

class SendCode(BaseResetPassword):
    def post(self, request):
        email = request.data['email']
        code = self.code_generator.code
        send_mail(
            "Password reset",
            f"Your password reset code is {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        return HttpResponse("Password reset email has been sent.")
class ResetPassword(BaseResetPassword):
    def post(self, request):
        code = request.data['code']
        if not self.code_generator.validate(code):
            print('code not matched or expired, ur code is ', self.code_generator.code)
            return HttpResponse("Invalid code", status=400)
        else:
            return HttpResponse("Your code matched. You can now reset your password.")

class HelloView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return HttpResponse("Hello, world!")
class GoogleLogin(GenericAPIView):
    serializer_class = TokenSerializer
    def post(self, request):
        access_token = request.data.get('access_token')
        data = requests.get(f"https://www.googleapis.com/oauth2/v2/userinfo", headers={
            "Authorization": f"Bearer {access_token}"
        }).json()
        print(data)
        user =  User.objects.get_or_create(username=data['email'])[0]
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        data = {
            'refresh': str(refresh),
            'access': str(access),
        }

        serializer = TokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        json = JSONRenderer().render(serializer.data)
        return HttpResponse(json, status=200)
    

