from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignupView.as_view(traveller=False), name='signup'),
    path('signup/traveller/', views.SignupView.as_view(traveller=True), name='signup_traveller'),
    path('signup/email/', views.EmailSignupView.as_view(traveller=False), name='email_signup'),
    path('signup/email/traveller/', views.EmailSignupView.as_view(traveller=True), name='email_signup_traveller'),
    path('signup/social-confirm/', views.SocialConfirmView.as_view(traveller=False), name='social_confirm'),
    path('signup/social-confirm/traveller/', views.SocialConfirmView.as_view(traveller=True), name='social_confirm_traveller'),
    path('signup/already/', views.AlreadyRegisteredView.as_view(), name='already_registered'),
    path('signup/complete/', views.CompleteView.as_view(), name='complete'),
    path('signup/activate/<uuid:uuid>/', views.ActivateView.as_view(), name='activate'),
    path('signup/activate/error/', views.ActivateErrorView.as_view(), name='activate_error'),
    path('signup/activate/again/', views.ActivateAgainView.as_view(), name='activate_again'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/traveller/', views.ProfileTravellerView.as_view(), name='profile_traveller'),
]
