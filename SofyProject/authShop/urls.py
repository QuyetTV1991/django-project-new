from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.handledLogin, name="handledLogin"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.handledLogout, name="handledLogout"),
    path("activate/<uidb64>/<token>", views.ActivateAccountView.as_view(), name='activate')
]