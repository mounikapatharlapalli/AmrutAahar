from django.shortcuts import redirect

def logout_user(request):
    request.session.clear()  # Clears all session data
    return redirect('/')
