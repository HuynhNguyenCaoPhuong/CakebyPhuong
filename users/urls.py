from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('my-account/',views.my_account, name='my-account'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
]
