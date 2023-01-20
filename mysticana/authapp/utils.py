from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as \
    token_generator


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    # print(user.__dict__)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    # if user.first_name:
    #     context['user'] = user.first_name
    # else:
    #     context['user'] = user.username
    # print(context)
    message = render_to_string(
        'authapp/verify_email.html',
        context=context,
    )
    # ???
    email = EmailMessage(
        'Veryfi email',
        message,
        to=[user.email],
    )
    print(message)
    email.send()