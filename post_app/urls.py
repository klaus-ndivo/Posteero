from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', lambda request: render(request, 'post_app/home.html'), name='home'),
    path('login/', LoginView.as_view(template_name='post_app/login.html', redirect_authenticated_user=True), name='login'),
    path('signup/', views.signup, name='signup'),
    path('mine/', views.mine, name='mine'),  # <-- use the new view here
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='post_app/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='post_app/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='post_app/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='post_app/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('frames/', views.frames, name='frames'),
    path('editor/<str:frame_type>/', views.editor, name='editor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)