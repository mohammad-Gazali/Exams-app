from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from main.forms import SendingEmailForm, CreateNormalUserForm
from main.models import NormalUser, Teacher



def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, 'about_us.html')


def contact(request: HttpRequest) -> HttpResponse:

    form = SendingEmailForm()

    sended = False

    if request.method == "POST":
        form = SendingEmailForm(request.POST)

        if form.is_valid():

            if not request.user.is_authenticated:
                form.add_error(field=None, error=_("Please Login Firstly, You Should Login Before Sending a Contact Email."))


            else:
                subject = form.cleaned_data.get("subject")
                message = form.cleaned_data.get("message")


                msg_html = render_to_string('email/contact.html', {
                    "subject": subject,
                    "message": message
                    })

                send_mail(
                    subject=subject,
                    html_message=msg_html,
                    message=msg_html,
                    from_email=request.user.email, # type: ignore
                    recipient_list= [settings.CONTACT_EMAIL]
                )

                sended = True

                form = SendingEmailForm()


    return render(request, 'contact.html', {"form": form, "sended": sended})


def support(request: HttpRequest) -> HttpResponse:
    return render(request, 'support.html')


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    normal_user = NormalUser.objects.filter(user=request.user)

    if normal_user:
        return render(request, "profile/profile_main.html", {"normal_user": normal_user.first()})
    
    else:
        form = CreateNormalUserForm()
        if request.method == "POST":
            form = CreateNormalUserForm(request.POST, request.FILES)

            if form.is_valid():
                normal_user = NormalUser.objects.create(
                    gender=form.cleaned_data["gender"],
                    nationality=form.cleaned_data["nationality"],
                    birthdate=form.cleaned_data["birthdate"],
                    phone_number=form.cleaned_data["phone_number"],
                    personal_image=form.cleaned_data["personal_image"],
                    user_id=request.user.id  # type: ignore
                )

                return render(request, "profile/profile_main.html", {"normal_user": normal_user})

        return render(request, "profile/profile_make.html", {"form": form})