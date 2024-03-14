from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .models import User

class LoginView(View):
    def get(self, request):
        return render(request, 'auth-login-basic.html')

    def post(self, request):
        user = authenticate(
            username=request.POST.get("email-username"),
            password=request.POST.get("password")
        )
        if user is None:
            return redirect("/user/login/")
        login(request, user)
        return redirect('/')




class RegisterView(View):
    def get(self, request):
        return render(request, 'auth-register-basic.html')

    def post(self, request):
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            error_message = 'This username is already taken.'
            return render(request, 'auth-register-basic.html', {'error_message': error_message})
        else:
            user = User.objects.create_user(
            username=username,
            password=request.POST.get("password"),
            email=request.POST.get("email"),
            is_staff=False,
            is_active=True,
            is_superuser=False,
        )
        login(request, user)
        return redirect("/user/profile")


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'auth-forgot-password-basic.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/user/login/')

class ProfileView(View):
    def get(self, request):
        context = {
            "user": request.user
        }
        return render(request, 'pages-account-settings-account.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            if request.POST.get("firstName"):
                user.first_name = request.POST.get("firstName")
            if request.POST.get("lastName"):
                user.last_name = request.POST.get("lastName")
            if request.POST.get("email"):
                user.email = request.POST.get("email")
            if request.FILES.get("photo"):
                user.picture = request.FILES.get("photo")
            if request.POST.get("organization"):
                user.organization = request.POST.get("organization")
            if request.POST.get("phoneNumber"):
                user.phone = request.POST.get("phoneNumber")
            if request.POST.get("address"):
                user.address = request.POST.get("address")
            if request.POST.get("district"):
                user.district = request.POST.get("district")
            if request.POST.get("region"):
                user.region = request.POST.get("region")
            user.save()
            return redirect('/user/profile')
        return redirect('/user/login')