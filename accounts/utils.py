from django.core.mail import send_mail

def verify_email(email,otp):
    subject = 'Email verification'
    message = f'Your Email verification Code is {otp}'
    from_email = 'ritesh@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)