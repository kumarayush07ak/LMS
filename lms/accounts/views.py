from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SignupUser, LoginRecord
from django.contrib.auth.hashers import make_password, check_password



def home(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    try:
        user = SignupUser.objects.get(id=user_id)
    except SignupUser.DoesNotExist:
        # session exists but user doesn't → clear session
        request.session.flush()
        return redirect('login')

    return render(request, 'home.html', {'user': user})



def signup_view(request):
    if request.method == "POST":
        first = request.POST['first_name']
        
        email = request.POST['email']
        phone = request.POST.get('phone')
        
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if SignupUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = SignupUser.objects.create(
            full_name=first,
            
            email=email,
            phone=phone,
            
            username=username,
            password=make_password(password)  # 🔐 hashed
        )

        LoginRecord.objects.create(user=user)

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = SignupUser.objects.get(username=username)
        except SignupUser.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('login')

        if check_password(password, user.password):
            # session login
            request.session['user_id'] = user.id

            # update login table
            LoginRecord.objects.filter(user=user).update()

            return redirect('home')
        else:
            messages.error(request, "Invalid password")

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')

        

# Create your views here.
