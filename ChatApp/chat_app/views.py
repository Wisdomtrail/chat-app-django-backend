import json
import random

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
        User.objects.all()

        return JsonResponse('successful', safe=False)
    else:
        return JsonResponse('Invalid', safe=False)


@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_profiles = []
        for user in users:
            user_profiles.append({
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number
            })
        return JsonResponse(user_profiles, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def setUserProfile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        profile_picture = request.FILES.get('profile_picture')
        print(username)
        print(profile_picture)
        if username and profile_picture:
            try:
                user = User.objects.get(username=username)
                user.profile_picture = profile_picture
                user.save()
                return JsonResponse({'message': 'Profile picture saved successfully'})
            except User.DoesNotExist:
                return JsonResponse({'message': 'User does not exist'}, status=404)
        else:
            return JsonResponse({'message': 'Missing username or profile picture'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
