from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    # Sending an email
    try:
        # Sending emails to admins
        mail_admins('subject', 'message', html_message='message')
        # send_mail('subject', 'message', 'info@daavo.com', ['bren@daavo.com'])
    except BadHeaderError:
        # Returning an error to the client in this case we pass
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
