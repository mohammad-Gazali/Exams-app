from django.shortcuts import render
from django.contrib.auth import login
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpRequest
from verify_email.email_handler import send_verification_email
from .forms import SignUpCustomForm



def register(request: HttpRequest):
    form = SignUpCustomForm()

    if request.method == "POST":
        form = SignUpCustomForm(request.POST)

        # login(request, object, backend=settings.AUTHENTICATION_BACKENDS[0])

        if form.is_valid():
            inactive_user = send_verification_email(request, form)

            return render(request, 'registration/go_to_verify.html', {"email": form.cleaned_data.get("email")})

    return render(request, 'registration/sign_up.html', {"form": form})


# class RegisterView(CreateView):
#     form_class = SignUpCustomForm
#     template_name = 'registration/sign_up.html'
    
#     def get_success_url(self):
#         login(self.request, self.object, backend=settings.AUTHENTICATION_BACKENDS[0])
#         return reverse_lazy('home')
    
#     def form_valid(self, form):
#         return super().form_valid(form)