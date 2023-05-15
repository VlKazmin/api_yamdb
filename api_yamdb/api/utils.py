from django.core.mail import send_mail


def send_confirmation_code(email, code):
    """Функция отправки сообщений."""
    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {code}"
    from_email = "your_email@example.com"
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
