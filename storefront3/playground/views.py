from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    # Sending an email
    try:
        # Creating EmailMessage object
        message = EmailMessage('subject', 'message', 'from@daavo.com', ['bren@daavo.com'])
        # Give the method the path relative to our project directory
        message.attach_file('playground/static/images/dog.jpeg')
        message.send()
    except BadHeaderError:
        # Returning an error to the client in this case we pass
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
