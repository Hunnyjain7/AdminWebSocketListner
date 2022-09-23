from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import ugettext_lazy as _
from .models import UserRole, User


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile_image = request.FILES.get("profile_image")

        print(name, email, password, profile_image)

        user = User(name=name, email=email, password=password, profile_image=profile_image)
        user.save()
        if user:
            return redirect('login')
        else:
            return redirect('register')


def logIn(request):
    try:
        if 'id' in request.session:
            return redirect('/dashboard')
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = User.objects.filter(email=email).filter(password=password)
            if not user:
                return redirect("/")
            user_id = user.get().id

            role = UserRole.objects.get(user_id=user_id)
            if role.role_id.role_name == 'User':
                request.session['id'] = user_id
                return redirect('/dashboard')
            else:
                return redirect("/")
        return render(request, 'login.html')
    except Exception as E:
        print(E)
        return render(request, 'logIn.html')


def adminLogIn(request):
    try:
        if 'id' in request.session:
            return redirect('/admin_dashboard')
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = User.objects.filter(email=email).filter(password=password)
            if not user:
                return redirect("/admin_login")
            user_id = user.get().id

            role = UserRole.objects.get(user_id=user_id)

            if role.role_id.role_name == 'Admin':
                request.session['id'] = user_id
                return redirect('/admin_dashboard')
            else:
                return redirect("/")
        return render(request, 'adminlogin.html')  # noqa
    except Exception as E:
        print(E)
        return render(request, 'adminlogin.html')  # noqa


def dashboard(request):
    try:
        return render(request, 'dashboard.html')
    except Exception as E:
        print(E)
        return render(request, 'login.html')


def adminDashboard(request):
    try:
        return render(request, 'admindashboard.html')  # noqa
    except Exception as E:
        print(E)
        return render(request, 'adminlogin.html')  # noqa


# def simpleGeneratorFun(request):
#     print("req", request)
#     yield JsonResponse({"status", "cool 1"})
#     yield JsonResponse({"status", "cool 2"})
#     yield JsonResponse({"status", "cool 3"})
#     yield JsonResponse({"status", "cool 4"})

# Driver code to check above generator function
# for value in simpleGeneratorFun():
#     print(value)
