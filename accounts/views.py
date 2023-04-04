from django.shortcuts import render
from django.http import HttpRequest
from verify_email.email_handler import send_verification_email
from accounts.forms import SignUpCustomForm



#? ===========================
#? ==== Important Note =======
#? ===========================
#? I disabled the messages that "allauth" package generate in the admin panel by adding empty text file called "logged_in.txt" inside "templates" folder in this directory: "templates/account/messages/logged_in.txt"
#? - taked from github: https://github.com/pennersr/django-allauth/issues/1455
#? ===========================
#? ===========================



def register(request: HttpRequest):
    form = SignUpCustomForm()

    if request.method == "POST":
        form = SignUpCustomForm(request.POST)

        if form.is_valid():

            inactive_user = send_verification_email(request, form)

            return render(request, 'registration/go_to_verify.html', {"email": form.cleaned_data.get("email")})

    return render(request, 'registration/sign_up.html', {"form": form})