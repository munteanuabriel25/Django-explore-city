from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as tk_generator
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

class EmailHandlerMixin:
    
    
    def send_activation_email(self,request,user):
        current_site = get_current_site(request)
        mail_subject = "Activate your account on " + str(current_site)
        message = render_to_string('user_profile/mail_activate_account.html',
                                   {'user': user.username,
                                    'domain': current_site.domain,
                                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token' : tk_generator.make_token(user)})
        
        email = EmailMessage(subject=mail_subject, body=message,to=[user.email])
        email.send()
        
        
        
    
    