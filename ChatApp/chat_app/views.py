import json
import random

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chat_app.models import User
from util.mail_sender import MailSender

confirmation_code = ""


@csrf_exempt
def signUp(request):
    global confirmation_code
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        password = data.get('password')
        confirmation_code = generateCode()
        user = User.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
        user.is_active = False

        email_subject = 'Account Confirmation'
        email_body = f'Hi {username},\n\n' \
                     f'Please use the following four-digit code to confirm your account: {confirmation_code}\n\n' \
                     f'Thank you!'
        mail_sender = MailSender()
        mail_sender.email_alert(email_subject, email_body, email)
        user.is_active = True
        return JsonResponse(
            {'message': 'User created successfully. Please check your email for the confirmation code.'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


def generateCode():
    return str(random.randint(1000, 9999))


@csrf_exempt
def confirmCode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        if code == confirmation_code:
            return JsonResponse({'message': 'Code matched successfully'})
        else:
            return JsonResponse({'message': 'Invalid confirmation code'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.kwargs['username']
        password = request.kwargs['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        return JsonResponse('successful', safe=False)
    else:
        return JsonResponse('Invalid', safe=False)
