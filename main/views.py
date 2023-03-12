from django.shortcuts import render
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import SendingEmailForm



def index(request: HttpRequest):
    return render(request, 'index.html')


def about_us(request: HttpRequest):
    return render(request, 'about_us.html')


def contact(request: HttpRequest):

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
                    from_email=request.user.email,
                    recipient_list= [settings.CONTACT_EMAIL]
                )

                sended = True

                form = SendingEmailForm()


    return render(request, 'contact.html', {"form": form, "sended": sended})


def support(request: HttpRequest):
    return render(request, 'support.html')