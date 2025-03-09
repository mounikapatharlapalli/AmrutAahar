from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views import View
from shop.models.customer import Customer

class SignUpView(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        first_name = request.POST.get('fn', '').strip()
        last_name = request.POST.get('ln', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        password = request.POST.get('password', '').strip()

        error_msg = None

        if Customer.objects.filter(email=email).exists():
            error_msg = "Email already exists."
        elif not first_name:
            error_msg = "First Name cannot be empty."
        elif not last_name:
            error_msg = "Last Name cannot be empty."
        elif not email:
            error_msg = "Email cannot be empty."
        elif not mobile:
            error_msg = "Mobile cannot be empty."
        elif not password:
            error_msg = "Password cannot be empty."

        if error_msg:
            return render(request, "signup.html", {'error': error_msg})
        
        # Save customer with hashed password
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            password=make_password(password)
        )
        customer.save()

        return redirect('/signin')  # Redirect to the login page
