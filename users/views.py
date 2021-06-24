from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import update_last_login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserModel
from .serializers import LoginSerializer, MyTokenObtainPairSerializer, UserLoginSerializer
from .forms import UserRegisterForm, UserUpdateForm
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        form = UserRegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # if UserModel.objects.get(username=form.cleaned_data['username']):
            #     res = ValidationError({'message': "Username already taken"})
            #     res.status_code = 409
            #     raise res
            form.save()
            return redirect('login')

# class RegisterView(APIView):
#     permission_classes = (AllowAny,)
#     # Allow any user (authenticated or not) to hit this endpoint.
#     template_name = 'users/register.html'
#     renderer_classes = [TemplateHTMLRenderer]
#
#     def get(self, request):
#         serializer = RegisterUserSerializer()
#         return Response({'serializer': serializer})
#
#     def post(self, request):
#         serializer = RegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 json = serializer.data
#                 return redirect('login')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    template_name = "users/login.html"
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        form = AuthenticationForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if not user:
                return Response("Invalid credentials", status=status.HTTP_400_BAD_REQUEST)
            else:
                login(request, user)
                user = UserModel.objects.get(username=username)
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                print(f"Access token: {access_token}")

                response = redirect("/profile/")
                # set cookie expiry to 5 minutes
                response.set_cookie(key="jwt", value=access_token, httponly=True, max_age=300)
                response.data = {
                    "jwt": access_token
                }
                return response


class ProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        user = UserModel.objects.get(username=request.user)
        return render(request, "users/profile.html", {"user": user.__dict__})


class ProfileEditView(APIView):
    def get(self, request, key):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        if key in ['id', 'date_joined', 'last_login', 'is_staff', 'is_superuser','is_admin', 'is_active']:
            return Response('Cannot edit item', status=status.HTTP_403_FORBIDDEN)
        form = UserUpdateForm()
        return render(request, 'users/profile-edit.html', {"key":key, "form": form})

    def post(self, request, key):
        form = UserUpdateForm(request.POST)
        user_obj = UserModel.objects.get(username=request.user)
        if form.is_valid():
            # print(form.cleaned_data['update_value'])
            setattr(user_obj, f"{key}", form.cleaned_data['update_value'])
            user_obj.save()
            return redirect('profile')


class ProfileClearAttr(APIView):
    def get(self, request, key):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        if key in ['id', 'date_joined', 'last_login', 'is_staff', 'is_superuser','is_admin', 'is_active']:
            return Response('Cannot delete item', status=status.HTTP_403_FORBIDDEN)
        user_obj = UserModel.objects.get(username=request.user)
        setattr(user_obj, f"{key}", "")
        user_obj.save()
        return redirect('profile')


def LogoutView(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response