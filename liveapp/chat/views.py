from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CampusNetwork
from .utils import get_client_ip  # Updated from SignUpForm
from .models import CampusNetwork
from .utils import get_client_ip
from .utils import get_client_ip  # The dot (.) means "look in the current folder"

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # Use the correct class name
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically logs the student in after signup
            return redirect('chat_room')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def chat_room(request):
    # Only authenticated users (students) can access the video chat
    return render(request, 'chat/index.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def chat_room(request):
    user_ip = get_client_ip(request)
    
    # Check if the student's current IP is in our campus list
    is_on_campus = CampusNetwork.objects.filter(public_ip=user_ip).exists()
    
    return render(request, 'chat/index.html', {
        'network_id': user_ip,
        'on_campus': is_on_campus
    })



@login_required
def chat_room(request):
    user_ip = get_client_ip(request)
    
    # Check if the student's current IP is in our campus list
    is_on_campus = CampusNetwork.objects.filter(public_ip=user_ip).exists()
    
    return render(request, 'chat/index.html', {
        'network_id': user_ip,
        'on_campus': is_on_campus
    })