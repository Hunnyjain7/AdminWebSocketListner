from django.shortcuts import render, redirect

# Create your views here.
from .models import UserRole, User


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
            print(role)

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
            return redirect('/admindashboard')
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = User.objects.filter(email=email).filter(password=password)
            if not user:
                return redirect("/")
            user_id = user.get().id

            role = UserRole.objects.get(user_id=user_id)

            if role.role_id.role_name == 'Admin':
                request.session['id'] = user_id
                return redirect('admindashboard')
            else:
                return redirect("/")
        return render(request, 'adminlogin.html')
    except Exception as E:
        print(E)
        return render(request, 'adminlogin.html')


def dashboard(request):
    try:
        return render(request, 'dashboard.html')
    except Exception as E:
        print(E)
        return render(request, 'logIn')


def adminDashboard(request):
    try:
        return render(request, 'admindashboard.html')
    except Exception as E:
        print(E)
        return render(request, 'adminlogin.html')
