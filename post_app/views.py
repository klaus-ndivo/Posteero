from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile, Design

# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password != password_confirmation:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'post_app/signup.html')

def login(request):
    return render(request, 'post_app/login.html')

@login_required
def update_profile(request):
    # Ensure the profile exists for the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('update_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'post_app/update_profile.html', context)

@login_required
def profile(request):
    return render(request, 'post_app/profile.html')

@login_required
def dashboard(request):
    designs = Design.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'post_app/dashboard.html', {'designs': designs})

@login_required
def mine(request):
    designs = Design.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'post_app/mine.html', {'designs': designs})

@login_required
def frames(request):
    frame_samples = [
        {"name": "Poster", "img": "poster_sample.jpg"},
        {"name": "Flyer", "img": "flyer_sample.jpg"},
        {"name": "Business Card", "img": "business_card_sample.jpg"},
        {"name": "Invitation", "img": "invitation_sample.jpg"},
        {"name": "Social Media Post", "img": "social_media_sample.jpg"},
        {"name": "Certificate", "img": "certificate_sample.jpg"},
        {"name": "Resume", "img": "resume_sample.jpg"},
        {"name": "Banner", "img": "banner_sample.jpg"},
        {"name": "Brochure", "img": "brochure_sample.jpg"},
        {"name": "Menu", "img": "menu_sample.jpg"},
        {"name": "Greeting Card", "img": "greeting_card_sample.jpg"},
        {"name": "Calendar", "img": "calendar_sample.jpg"},
        {"name": "Newsletter", "img": "newsletter_sample.jpg"},
        {"name": "Magazine Cover", "img": "magazine_sample.jpg"},
        {"name": "ID Card", "img": "id_card_sample.jpg"},
        # Add more as needed
    ]
    return render(request, 'post_app/frames.html', {'frames': frame_samples})

@login_required
def editor(request, frame_type):
    return render(request, 'post_app/editor.html', {'frame_type': frame_type})