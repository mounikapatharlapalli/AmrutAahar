from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib import messages
from shop.models.customer import Customer

class SignInView(View):
    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.GET.get('next', 'home')  # Redirect to checkout if needed

        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            user = None

        if user and user.check_password(password):  # Use Django's check_password
            request.session['customer_id'] = user.id
            request.session['customer_email'] = user.email
            messages.success(request, "Logged in successfully!")
            return redirect(next_url)  # Redirect to checkout if applicable
        
        messages.error(request, "Invalid email or password!")
        return render(request, 'signin.html', {'error': "Invalid email or password!"})
