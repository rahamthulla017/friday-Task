from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import CsrfViewMiddleware
from django.template import loader
from django.http import HttpResponse

def login_page(request):
    return render(request, 'login.html')

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Log the user into the Django session so server-rendered pages
            # (like /profile/) will recognize the authenticated user.
            try:
                # request is a DRF Request; use the underlying HttpRequest for login
                login(request._request, user)
            except Exception:
                # If session middleware is not present or login fails, continue
                pass
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def profile_page(request):
    """Simple profile page that shows username and role if the user is authenticated.

    Note: In this project authentication is via JWT for the API; the template view will
    rely on Django session authentication if used in-browser. For simplicity this page
    will show whatever is available on request.user (AnonymousUser otherwise).
    """
    user = request.user
    return render(request, 'profile.html', {'user': user})


def register_page(request):
    # GET -> render register page
    if request.method == 'GET':
        return render(request, 'register.html')

    # POST -> handle form submission
    data = request.POST.dict()
    serializer = UserRegistrationSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        try:
            login(request, user)
        except Exception:
            pass
        return redirect('profile')

    return render(request, 'register.html', {'form_errors': serializer.errors, 'form_data': data})
