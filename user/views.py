from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserModel
from .serializers import CustomUserSerializer, LoginSerializer
from .forms import UserRegisterForm


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    # Allow any user (authenticated or not) to hit this endpoint.
    template_name = 'user/register.html'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        serializer = CustomUserSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return redirect('login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    template_name = "user/login.html"
    renderer_classes = [TemplateHTMLRenderer]


    def get(self, request):
        serializer = LoginSerializer()
        return Response({"serializer":serializer})

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        update_last_login(None, user)
        token = serializer.get_token(user)
        print(token)
        return redirect('profile')


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = UserModel.objects.get(username=request.user)
        return render(request, 'user/profile.html', {'user': user.__dict__})