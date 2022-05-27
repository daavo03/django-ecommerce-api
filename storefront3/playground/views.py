from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    # Sending an email
    try:
        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Daavo'}
        )
        message.send(['bren@daavo.com'])
    except BadHeaderError:
        # Returning an error to the client in this case we pass
        pass
    return render(request, 'hello.html', {'name': 'Daavo'})
