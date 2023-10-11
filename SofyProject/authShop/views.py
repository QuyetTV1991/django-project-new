from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import View
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import generate_token, TokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def handledLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Success")
            return redirect('index')

        else:
            messages.error(request, "Invalid Credential")
            return redirect('handledLogin')

    return render(request, 'myShop/login.html')


def handledLogout(request):
    logout(request)
    messages.success(request, "Logout Success")

    return redirect('index')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request, "Password is not matching")
            return redirect('signup')

        try:
            if User.objects.get(Q(username=username) | Q(email=email)):
                messages.warning(request, "User/Email was taken already")
                return redirect('signup')
        except Exception as indentifier:
            pass

        user = User.objects.create_user(username, email, password1)
        user.is_active = False
        user.save()

        email_subject = 'Activate Your Account'
        mail_content = render_to_string('myWebsite/activate.html', {
            'user': user,
            'domain': 'https://localhost:8000', # consider to use correct domain
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email_message = EmailMessage(
            email_subject, mail_content, settings.EMAIL_HOST_USER, [email]
        )
        email_message.send()
        messages.success(request, "An email to verify was sent to your email")

        return redirect('handledLogin')

    return render(request, 'myShop/signup.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as indentifier:
            user=None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('handledLogin')
        return render(request, 'myShop/activatefail.html')